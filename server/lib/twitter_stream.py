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
                            
## for test
if __name__ == '__main__':
    follow = "3699404474"
    for item in TwitterStream.get(follow=[follow]):
        print item["text"]
        try:
            for hashtag in item["entities"]["hashtags"]:
                print "hashtag"
                print hashtag["text"]
            #print "multi media"
            #for media in item["extended_entities"]["media"]:
            #    print media["media_url_https"]

        except KeyError:
            print item["entities"]
