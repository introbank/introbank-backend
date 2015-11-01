# -*- coding: utf-8 -*-
from twitter_util import TwitterUtil
from parse_connection import ParseConnection

class MediaTableData(object):
    tableName = "Media"

    def insert(cls, twitterId, twitterStatusId, mediaUri, info):
        connection = ParseConnection()
        dataDict = {"twitterId": str(twitterId),
                "twitterStatusId": str(twitterStatusId),
                "mediaUri": mediaUri, 
                "info": info}
        connection.connect()
        res = connection.insert(cls.tableName, dataDict)
        return res
