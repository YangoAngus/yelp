# -*- coding: utf-8 -*-
import scrapy
from yelp_scrapy.items import YelpScrapyItem
from yelp_scrapy.models import init_db


class YelpSpider(scrapy.Spider):
    name = 'yelp'

    def __init__(self):
        init_db()

    def start_requests(self):
        urls = [
            'https://www.yelp.com/search?cflt=restaurants&find_loc=Los%20Angeles%2C%20CA',
            'https://www.yelp.com/search?cflt=gyms&find_loc=Los%20Angeles%2C%20CA',
            'https://www.yelp.com/search?cflt=massage&find_loc=Los%20Angeles%2C%20CA',
            'https://www.yelp.com/search?cflt=restaurants&find_loc=New%20York%2C%20NY',
            'https://www.yelp.com/search?cflt=gyms&find_loc=New%20York%2C%20NY',
            'https://www.yelp.com/search?cflt=massage&find_loc=New%20York%2C%20NY',
            'https://www.yelp.com/search?cflt=restaurants&find_loc=San%20Francisco%2C%20CA',
            'https://www.yelp.com/search?cflt=gyms&find_loc=San%20Francisco%2C%20CA',
            'https://www.yelp.com/search?cflt=massage&find_loc=San%20Francisco%2C%20CA',
            ]
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.in_category
                )

    def in_category(self, response):
        for i in response.xpath(
            '//div[@class="lemon--div__373c0__1mboc '
            'border-color--default__373c0__3-ifU"]'
            '//h4[@class="lemon--h4__373c0__1yd__ '
            'heading--h4__373c0__27bDo '
            'alternate__373c0__2Mge5"]'
            '//a[@class="lemon--a__373c0__IEZFH '
            'link__373c0__1G70M '
            'link-color--inherit__373c0__3dzpk '
            'link-size--inherit__373c0__1VFlE"]/@href'
            ).extract():
            yield scrapy.Request(
                url=response.urljoin(i),
                callback=self.inner_page,
                meta={
                    'location': response.url.split('%20')[-1].split('&')[0],
                    'category': response.url.split('cflt=')[1].split('&')[0],
                }
            )
        next_page = response.xpath(
            '//a[@class="lemon--a__373c0__IEZFH '
            'link__373c0__1G70M next-link '
            'navigation-button__373c0__23BAT '
            'link-color--inherit__373c0__3dzpk '
            'link-size--inherit__373c0__1VFlE"]/@href'
        ).extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(
                url=next_page,
                callback=self.in_category
            )

    def inner_page(self, response):
        item = YelpScrapyItem()
        item['category'] = response.meta.get('category')
        item['location'] = response.meta.get('location')
        item['source_url'] = response.url
        item['title'] = response.css('h1::text').get()
        item['address'] = {'address': address.css(
            'span::text'
        ).getall() for address in response.css(
            'address.lemon--address__373c0__2sPac'
        )}
        item['timetable'] = {i[1].xpath(
            '//th/p/text()'
        ).extract()[i[0]]: i[1].xpath(
            '//td//p/text()'
        ).extract()[i[0]] for i in enumerate(
            [i for i in response.xpath('//tr')]
        )}
        item['telephone'] = [response.css('p')[i[0] + 1:].css(
            'p::text'
        ).get() for i in enumerate(response.css('p')) if i[1].css(
            'p::text'
        ).get() == 'Phone number']
        item['website'] = [response.css('p')[i[0] + 1].css(
            'a::text'
        ).get() for i in enumerate(response.css('p')) if i[1].css(
            'p::text'
        ).get() == 'Business website']
        item['about'] = [i for i in set([response.css('div')[i[0] + 1:].css(
            'span::text'
        ).get() for i in enumerate(response.css('div')) if i[1].css(
            'h4::text'
        ).get() == 'About the Business'])]
        item['images'] = [i for i in response.xpath(
            '//div[@data-testid="photoHeader"]//img/@src'
        ).extract()]
        reviews = response.xpath(
            '//span[@class="lemon--span__373c0__3997G text__373c0__2Kxyz '
            'text-color--black-extra-light__373c0__2OyzO '
            'text-align--left__373c0__2XGa-"]/text()'
        ).extract_first()
        item['reviews'] = int(
            reviews.split(' ')[-1]
        ) * 20 if reviews else reviews is 0
        yield item