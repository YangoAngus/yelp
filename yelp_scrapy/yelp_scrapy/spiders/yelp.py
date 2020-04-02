# -*- coding: utf-8 -*-
import scrapy
from yelp_scrapy.items import YelpScrapyItem

item = YelpScrapyItem()


class YelpSpider(scrapy.Spider):
    name = 'yelp'
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
        for i in response.xpath('//div[@class="lemon--div__373c0__1mboc border-color--default__373c0__3-ifU"]//h4[@class="lemon--h4__373c0__1yd__ heading--h4__373c0__27bDo alternate__373c0__2Mge5"]//a[@class="lemon--a__373c0__IEZFH link__373c0__1G70M link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE"]/@href').extract():
            yield scrapy.Request(
                url=response.urljoin(i),
                callback=self.inner_page,
                )
            
    def inner_page(self, response):
        item['title'] = response.css('h1::text').get()
        item['address'] = response.css('address.lemon--address__373c0__2sPac::text').get()
        print(item['title'])
