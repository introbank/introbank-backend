# -*- coding: utf-8 -*-
import twitter

class TwitterUtil(object):
    CONSUMER_KEY = "LZXKM3AFHSWWy7c9EVJu90kYZ"
    CONSUMER_SECRET = "bxR8uOR1FgHLLa0g4gdbNrmu465Qb5Nsd0E14afGExmTKZ7PRV" 
    ACCESS_TOKEN_KEY = "3699404474-aGC4yBOzlXPCmXinDPzrPZdN3yAJb3V03HLOdls"
    ACCESS_TOKEN_SECRET = "m4AVTdJHknG0qYnkQEgVbMVhQhWfmBLbUuMmmv57R2ckP"
    STREAM_API_BASE_URL = "https://stream.twitter.com/1.1"

    @classmethod
    def getApiInstance(cls, base_url):
        return twitter.Api(base_url=base_url,
                          consumer_key=cls.CONSUMER_KEY,
                          consumer_secret=cls.CONSUMER_SECRET,
                          access_token_key=cls.ACCESS_TOKEN_KEY,
                          access_token_secret=cls.ACCESS_TOKEN_SECRET)

    @classmethod
    def getStreamApiInstance(cls):
        return cls.getApiInstance(cls.STREAM_API_BASE_URL)
