# -*- coding: utf-8 -*-

import scrapy
import urllib2
from datetime import datetime, time
from icalendar import Calendar
from datetime import datetime
from datetime import timedelta
from crawler.items import EventItem


class MosoclbrSpider(scrapy.Spider):
    name = "mosoclbr"
    start_urls = [
        "https://calendar.google.com/calendar/ical/moejapan.jp_0pchodm9tjiglln75nh31g7mb8%40group.calendar.google.com/public/basic.ics"
    ]

    def parse(self, response):
        ical_data = urllib2.urlopen(response.url).read()
        calendars = Calendar.from_ical(ical_data)

        for event in calendars.walk('vevent'):
            dtstart = event.decoded('dtstart')
            if datetime.combine(dtstart, time()) > datetime.now():
                item = EventItem()
                item['objectId'] = 'KHsovBg9CZ'
                item['title'] = event['summary'].encode('utf-8')
                item['detail'] = event['description'].encode('utf-8')
                datetimeData = event.decoded('dtstart')
                datetimeData = datetimeData - timedelta(hours=9)
                item['date'] = datetimeData.strftime('%Y-%m-%dT%H:%M:%S')
                item['place'] = event['location'].encode('utf-8')
                item['charge'] = ''
                yield item
