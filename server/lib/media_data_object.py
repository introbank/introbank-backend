# -*- coding: utf-8 -*-
from base_data_object import BaseDataObject

class MediaDataObject(BaseDataObject):
    tableName = "Media"

    def insert(self, twitterId, twitterStatusId, mediaUri, tweetObjectId):
        dataDict = {}
        dataDict = {"twitterId": str(twitterId),
                "twitterStatusId": str(twitterStatusId),
                "mediaUri": mediaUri,
                "tweet":{"__type":"Pointer", "className":"Tweet", "objectId":tweetObjectId}}
        
        return self._insert(dataDict)
