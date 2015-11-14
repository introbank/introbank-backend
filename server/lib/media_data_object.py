# -*- coding: utf-8 -*-
from base_data_object import BaseDataObject

class MediaDataObject(BaseDataObject):
    tableName = "Media"

    def insert(self, twitterId, twitterStatusId, mediaUri, info, hashtag = None):
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
        
        return self._insert(dataDict)
