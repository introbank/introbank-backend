# -*- coding: utf-8 -*-
from twitter_util import TwitterUtil
from parse_connection import ParseConnection

class MediaTableData(object):
    tableName = "Media"

    def __init__(self, twitterId, twitterStatusId, mediaUri, info):
        self.twitterId = twitterId
        self.twitterStatusId = twitterStatusId
        self.mediaUri = mediaUri
        self.info = info
  
    def insert(self):
        connection = ParseConnection()
        dataDict = {"twitterId": str(self.twitterId),
                "twitterStatusId": str(self.twitterStatusId),
                "mediaUri": self.mediaUri, 
                "info": self.info}
        connection.connect()
        res = connection.insert(self.tableName, dataDict)
        return res
