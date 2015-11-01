# -*- coding: utf-8 -*-
# easy_install python_twitter
from twitter_util import TwitterUtil
import dateutil.parser
import urllib

class TwitterStream(object):
    @classmethod
    def get(cls, follow=None, track=None):
        print "get api start"
        api = TwitterUtil.getStreamApiInstance()
        for item in api.GetStreamFilter(follow=follow, track=track):
            yield item
                            
if __name__ == '__main__':
    target = "#nhk"
    for item in TwitterStream.get(track=[target]):
        print item
