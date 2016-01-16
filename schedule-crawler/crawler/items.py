# -*- coding: utf-8 -*-

import scrapy


class EventItem(scrapy.Item):
    objectId = scrapy.Field()
    title = scrapy.Field()
    detail = scrapy.Field()
    date = scrapy.Field()
    place = scrapy.Field()
    charge = scrapy.Field()
