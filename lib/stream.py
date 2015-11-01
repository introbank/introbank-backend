# -*- coding: utf-8 -*-
# easy_install python_twitter
from twitter_util import TwitterUtil
import dateutil.parser

class TwitterStream(object):
    @classmethod
    def get(cls, follow=None, track=None):
        api = TwitterUtil.getStreamApiInstance()
        for item in api.GetStreamFilter(follow=follow, track=track):
            print '---------------------'
            if 'text' in item:
                print (item['id_str'])
                print (dateutil.parser.parse(item['created_at']))
                print (item['text'])
                print (item['place'])
     
if __name__ == '__main__':
    TwitterStream.get(track=["BiSH"]) 
