# -*- coding: utf-8 -*-
from twitter_util import TwitterUtil
from parse_connection import ParseConnection
from base_data_object import BaseDataObject

class MediaTableDataObject(BaseDataObject):
    tableName = "Media"

    def insert(cls, twitterId, twitterStatusId, mediaUri, info, hashtag = None):
        connection = ParseConnection()
        dataDict = {}
        if hashtag is None:
            dataDict = {"twitterId": str(twitterId),
                    "twitterStatusId": str(twitterStatusId),
                    "mediaUri": mediaUri,
                    "info": info}
        else:
            dataDict = {"twitterId": str(twitterId),
                    "twitterStatusId": str(twitterStatusId),
                    "mediaUri": mediaUri,
                    "info": info,
                    "hashtag":hashtag}

        connection.connect()
        res = connection.insert(cls.tableName, dataDict)
        return res
