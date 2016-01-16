# -*- coding: utf-8 -*-

import scrapy

from crawler.items import EventItem
from datetime import datetime
from datetime import timedelta


class PassCodeSpider(scrapy.Spider):
    name = "passcode"
    start_urls = ["http://passcode-official.com/schedule/"]

    def parse(self, response):
        for sel in response.xpath('//*[contains(@class,"scdBox")]'):
            item = EventItem()
            item['objectId'] = "veQfrIFTfs"
            item['title'] = sel.xpath('div/div/p[3]/text()')[0].extract()
            item['detail'] = "".join(sel.xpath('div/table/tr[1]/td/text()').extract()).replace("\t", "")
            item['place'] = sel.xpath('div/div/h3/text()')[0].extract()
            item['charge'] = sel.xpath('div/table/tr[4]/td/text()')[0].extract().replace("\n", "").replace("\t", "")
            datetimeStr = sel.xpath('div/div/p[1]/text()')[0].extract() + " " + sel.xpath('div/table/tr[3]/td/text()')[0].extract().split(" ")[2]
            datetimeData = datetime.strptime(datetimeStr, '%Y.%m.%d %H:%M') - timedelta(hours=9)
            item['date'] = datetimeData.strftime('%Y-%m-%dT%H:%M:00')

            yield item
