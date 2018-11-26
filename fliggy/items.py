# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FliggyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    triptype = scrapy.Field()
    dep_city = scrapy.Field()
    arr_city = scrapy.Field()
    first_dep_date = scrapy.Field()
    second_dep_date = scrapy.Field()
    lowest_price = scrapy.Field()



