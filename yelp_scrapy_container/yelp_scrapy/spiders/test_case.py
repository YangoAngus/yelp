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
        init_db()

    def start_requests(self):
        urls = [
            'file://{}/test_html.html'.format(os.getcwd())
            # 'https://www.yelp.com/biz/daves-hot-chicken-los-angeles', # this is a test_case source
            # 'https://www.yelp.com/biz/project-13-gyms-san-francisco',
            # 'https://www.yelp.com/biz/md-foot-massage-los-angeles-3',
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
            '//div[@class="lemon--div__373c0__1mboc '
            'padding-b2__373c0__34gV1 '
            'border-color--default__373c0__3-ifU '
            'text-align--center__373c0__2n2yQ"]/span/text()'
        ).extract_first()
        item['reviews'] = int(
            reviews.split(' ')[-1]
        ) * 20 if reviews else reviews is 0
        yield item


        address = response.css('address.lemon--address__373c0__2sPac').getall()
        test_data_address.extend(address)
        test_data_timetable.extend(response.xpath('//tr').extract())
        test_data_reviews.append(response.xpath(
            '//div[@class="lemon--div__373c0__1mboc '
            'padding-b2__373c0__34gV1 '
            'border-color--default__373c0__3-ifU '
            'text-align--center__373c0__2n2yQ"]/span'
        ).extract_first())


test_data_address = []
test_data_timetable = []
test_data_reviews = []



@pytest.fixture
def test_answer():
    process = CrawlerProcess()
    process.crawl(YelpTestSpider)
    process.start()


def test_1(test_answer):
    assert test_data_address == ['<address class="lemon--address__373c0__2sPac"><p class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa- text-weight--bold__373c0__1elNz"><span class="lemon--span__373c0__3997G raw__373c0__3rcx7">970 N Western Ave</span></p><p class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa- text-weight--bold__373c0__1elNz"><span class="lemon--span__373c0__3997G raw__373c0__3rcx7">Los Angeles, CA 90029</span></p></address>']
    assert test_data_timetable == ['<tr class="lemon--tr__373c0__14NN0 table-row__373c0__3wipe"><th class="lemon--th__373c0__2EYOe table-header-cell__373c0__3vHHa table-header-cell__373c0___pz7p" scope="col"><p class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa- text-weight--bold__373c0__1elNz">Mon</p></th><td class="lemon--td__373c0__gBfiC table-cell__373c0__HrAej table-cell__373c0__2eOj9 table-cell--top__373c0__2WIt-"><ul class="lemon--ul__373c0__1_cxs undefined list__373c0__2G8oH"><li class="lemon--li__373c0__1r9wz border-color--default__373c0__3-ifU"><p class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz no-wrap__373c0__2vNX7 text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-">11:30 am - 11:00 pm</p></li></ul></td><td class="lemon--td__373c0__gBfiC table-cell__373c0__HrAej table-cell__373c0__2eOj9 table-cell--top__373c0__2WIt-"></td></tr>', '<tr class="lemon--tr__373c0__14NN0 table-row__373c0__3wipe"><th class="lemon--th__373c0__2EYOe table-header-cell__373c0__3vHHa table-header-cell__373c0___pz7p" scope="col"><p class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa- text-weight--bold__373c0__1elNz">Tue</p></th><td class="lemon--td__373c0__gBfiC table-cell__373c0__HrAej table-cell__373c0__2eOj9 table-cell--top__373c0__2WIt-"><ul class="lemon--ul__373c0__1_cxs undefined list__373c0__2G8oH"><li class="lemon--li__373c0__1r9wz border-color--default__373c0__3-ifU"><p class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz no-wrap__373c0__2vNX7 text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-">11:30 am - 11:00 pm</p></li></ul></td><td class="lemon--td__373c0__gBfiC table-cell__373c0__HrAej table-cell__373c0__2eOj9 table-cell--top__373c0__2WIt-"></td></tr>', '<tr class="lemon--tr__373c0__14NN0 table-row__373c0__3wipe"><th class="lemon--th__373c0__2EYOe table-header-cell__373c0__3vHHa table-header-cell__373c0___pz7p" scope="col"><p class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa- text-weight--bold__373c0__1elNz">Wed</p></th><td class="lemon--td__373c0__gBfiC table-cell__373c0__HrAej table-cell__373c0__2eOj9 table-cell--top__373c0__2WIt-"><ul class="lemon--ul__373c0__1_cxs undefined list__373c0__2G8oH"><li class="lemon--li__373c0__1r9wz border-color--default__373c0__3-ifU"><p class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz no-wrap__373c0__2vNX7 text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-">11:30 am - 11:00 pm</p></li></ul></td><td class="lemon--td__373c0__gBfiC table-cell__373c0__HrAej table-cell__373c0__2eOj9 table-cell--top__373c0__2WIt-"><span class="lemon--span__373c0__3997G text__373c0__2Kxyz open-status__373c0__215Gm no-wrap__373c0__2vNX7 text-color--red__373c0__n7iaa text-align--left__373c0__2XGa- text-weight--bold__373c0__1elNz text-size--small__373c0__3NVWO">Closed now</span></td></tr>', '<tr class="lemon--tr__373c0__14NN0 table-row__373c0__3wipe"><th class="lemon--th__373c0__2EYOe table-header-cell__373c0__3vHHa table-header-cell__373c0___pz7p" scope="col"><p class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa- text-weight--bold__373c0__1elNz">Thu</p></th><td class="lemon--td__373c0__gBfiC table-cell__373c0__HrAej table-cell__373c0__2eOj9 table-cell--top__373c0__2WIt-"><ul class="lemon--ul__373c0__1_cxs undefined list__373c0__2G8oH"><li class="lemon--li__373c0__1r9wz border-color--default__373c0__3-ifU"><p class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz no-wrap__373c0__2vNX7 text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-">11:30 am - 11:00 pm</p></li></ul></td><td class="lemon--td__373c0__gBfiC table-cell__373c0__HrAej table-cell__373c0__2eOj9 table-cell--top__373c0__2WIt-"></td></tr>', '<tr class="lemon--tr__373c0__14NN0 table-row__373c0__3wipe"><th class="lemon--th__373c0__2EYOe table-header-cell__373c0__3vHHa table-header-cell__373c0___pz7p" scope="col"><p class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa- text-weight--bold__373c0__1elNz">Fri</p></th><td class="lemon--td__373c0__gBfiC table-cell__373c0__HrAej table-cell__373c0__2eOj9 table-cell--top__373c0__2WIt-"><ul class="lemon--ul__373c0__1_cxs undefined list__373c0__2G8oH"><li class="lemon--li__373c0__1r9wz border-color--default__373c0__3-ifU"><p class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz no-wrap__373c0__2vNX7 text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-">11:30 am - 12:00 am</p></li></ul></td><td class="lemon--td__373c0__gBfiC table-cell__373c0__HrAej table-cell__373c0__2eOj9 table-cell--top__373c0__2WIt-"></td></tr>', '<tr class="lemon--tr__373c0__14NN0 table-row__373c0__3wipe"><th class="lemon--th__373c0__2EYOe table-header-cell__373c0__3vHHa table-header-cell__373c0___pz7p" scope="col"><p class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa- text-weight--bold__373c0__1elNz">Sat</p></th><td class="lemon--td__373c0__gBfiC table-cell__373c0__HrAej table-cell__373c0__2eOj9 table-cell--top__373c0__2WIt-"><ul class="lemon--ul__373c0__1_cxs undefined list__373c0__2G8oH"><li class="lemon--li__373c0__1r9wz border-color--default__373c0__3-ifU"><p class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz no-wrap__373c0__2vNX7 text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-">11:30 am - 12:00 am</p></li></ul></td><td class="lemon--td__373c0__gBfiC table-cell__373c0__HrAej table-cell__373c0__2eOj9 table-cell--top__373c0__2WIt-"></td></tr>', '<tr class="lemon--tr__373c0__14NN0 table-row__373c0__3wipe"><th class="lemon--th__373c0__2EYOe table-header-cell__373c0__3vHHa table-header-cell__373c0___pz7p" scope="col"><p class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa- text-weight--bold__373c0__1elNz">Sun</p></th><td class="lemon--td__373c0__gBfiC table-cell__373c0__HrAej table-cell__373c0__2eOj9 table-cell--top__373c0__2WIt-"><ul class="lemon--ul__373c0__1_cxs undefined list__373c0__2G8oH"><li class="lemon--li__373c0__1r9wz border-color--default__373c0__3-ifU"><p class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz no-wrap__373c0__2vNX7 text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-">11:30 am - 12:00 am</p></li></ul></td><td class="lemon--td__373c0__gBfiC table-cell__373c0__HrAej table-cell__373c0__2eOj9 table-cell--top__373c0__2WIt-"></td></tr>']
    assert test_data_reviews == ['<span class="lemon--span__373c0__3997G text__373c0__2Kxyz text-color--black-extra-light__373c0__2OyzO text-align--left__373c0__2XGa-">1 of 157</span>']