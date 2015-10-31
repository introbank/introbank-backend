# -*- coding: utf-8 -*-
# easy_install python_twitter
import twitter
import dateutil.parser
import time

class TwitterStream(object):
    @classmethod
    def get(cls):
        consumer_key = "LZXKM3AFHSWWy7c9EVJu90kYZ"
        consumer_secret = "bxR8uOR1FgHLLa0g4gdbNrmu465Qb5Nsd0E14afGExmTKZ7PRV" 
        access_token_key = "3699404474-aGC4yBOzlXPCmXinDPzrPZdN3yAJb3V03HLOdls"
        access_token_secret = "m4AVTdJHknG0qYnkQEgVbMVhQhWfmBLbUuMmmv57R2ckP"
        follow = ["3699404474"]
        track = ["beatles"]
      
        api = twitter.Api(base_url="https://stream.twitter.com/1.1",
                          consumer_key=consumer_key,
                          consumer_secret=consumer_secret,
                          access_token_key=access_token_key,
                          access_token_secret=access_token_secret)

        for item in api.GetStreamFilter(follow=follow, track=track):
            print '---------------------'
            if 'text' in item:
                print (item['id_str'])
                print (dateutil.parser.parse(item['created_at']))
                print (item['text'])
                print (item['place'])
    
if __name__ == '__main__':
    while(True):
        try:
            TwitterStream.get() 
        except:
            time.sleep(1.5)
