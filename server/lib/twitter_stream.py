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
    follow = "3699404474"
    for item in TwitterStream.get(follow=[follow]):
        print item["text"]
        try:
            print "media"
            for media in item["entities"]["media"]:
                print media
            print "multi media"
            for media in item["extended_entities"]["media"]:
                print media

        except KeyError:
            print item["entities"]
