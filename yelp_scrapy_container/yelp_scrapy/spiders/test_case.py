# -*- coding: utf-8 -*-
import scrapy
from yelp_scrapy.items import YelpScrapyItem
import pytest
from scrapy.crawler import CrawlerProcess
import os
from yelp_scrapy.models import init_db


class YelpTestSpider(scrapy.Spider):
    name = 'test_case'

    def __init__(self):
        pass
        # init_db()

    def start_requests(self):
        urls = [
            # 'file://{}/test_html.html'.format(os.getcwd())
            # 'https://www.yelp.com/biz/daves-hot-chicken-los-angeles',
            # 'https://www.yelp.com/biz/project-13-gyms-san-francisco',
            # 'https://www.yelp.com/biz/md-foot-massage-los-angeles-3',
            'https://www.yelp.com/biz/crown-of-india-los-angeles-2'
            ]
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    'location': 'LA',
                    'category': 'Restaurant',
                },
            )

    def parse(self, response):
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


        test_data_address.append(response.css('address.lemon--address__373c0__2sPac').getall()[0].split('>')[0])
        test_data_reviews.append(response.xpath('//span[@class="lemon--span__373c0__3997G text__373c0__2Kxyz text-color--black-extra-light__373c0__2OyzO text-align--left__373c0__2XGa-"]').extract_first().split('>')[0])


test_data_address = []
test_data_reviews = []



@pytest.fixture
def test_answer():
    process = CrawlerProcess()
    process.crawl(YelpTestSpider)
    process.start()


def test_1(test_answer):
    assert test_data_address == ['<address class="lemon--address__373c0__2sPac"']
    assert test_data_reviews == ['<span class="lemon--span__373c0__3997G text__373c0__2Kxyz text-color--black-extra-light__373c0__2OyzO text-align--left__373c0__2XGa-"']