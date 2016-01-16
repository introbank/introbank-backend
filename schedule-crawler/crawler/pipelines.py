# -*- coding: utf-8 -*-

from crawler.parse_client import ParseClient


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        #print item
        ParseClient.insert_event(item)
