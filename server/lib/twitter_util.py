# -*- coding: utf-8 -*-
import twitter

class TwitterUtil(object):
    CONSUMER_KEY = "hoge"
    CONSUMER_SECRET = "moge" 
    ACCESS_TOKEN_KEY = "moga"
    ACCESS_TOKEN_SECRET = "fuga"
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
