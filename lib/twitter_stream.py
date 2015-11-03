# -*- coding: utf-8 -*-
# easy_install python_twitter
from twitter_util import TwitterUtil

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
