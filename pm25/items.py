# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Pm25Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    aqi = scrapy.Field()
    pm2_5 = scrapy.Field()
    co = scrapy.Field()
    pm10 = scrapy.Field()
    so2 = scrapy.Field()
    no2 = scrapy.Field()
    o3 = scrapy.Field()
    position_name = scrapy.Field()
    area = scrapy.Field()
    time_point = scrapy.Field()

