# -*- coding: utf-8 -*-
import scrapy
from yelp_scrapy.items import YelpScrapyItem

item = YelpScrapyItem()


class YelpTestSpider(scrapy.Spider):
    name = 'yelp_test'

    def start_requests(self):
        urls = [
            'https://www.yelp.com/biz/chd-los-angeles?osq=Restaurants',
            ]
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                )
                
    def parse(self, response):
        item['title'] = response.css('h1::text').get()
        for address in response.css('address.lemon--address__373c0__2sPac'):
            item['address'] = {'address': address.css('span::text').getall()}
        item['telephone'] = response.xpath('//p[@class="lemon--p__373c0__3Qnnj text__373c0__2pB8f text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_"]/text()').extract()[-1]
        print(item['title'])
        print(item['address'])
        print(item['telephone'])
        
