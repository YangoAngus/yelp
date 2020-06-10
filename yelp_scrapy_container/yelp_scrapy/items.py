# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    telephone = scrapy.Field()
    website = scrapy.Field()
    timetable = scrapy.Field()
    about = scrapy.Field()
    images = scrapy.Field()
    reviews = scrapy.Field()
    category = scrapy.Field()
    location = scrapy.Field()
    source_url = scrapy.Field()
    pass
