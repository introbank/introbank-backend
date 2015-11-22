# -*- coding: utf-8 -*-
from base_data_object import BaseDataObject

class TweetDataObject(BaseDataObject):
    tableName = "Tweet"

    def insert(self, twitterId, twitterStatusId, text, className, objectId, isReflected = False):
        dataDict = {"twitterId": str(twitterId),
                    "twitterStatusId": str(twitterStatusId),
                    "text":text,
                    "isReflected": isReflected}

        col = className.lower()
        pointer    = {"__type": "Pointer", "className":className, "objectId":objectId}
       
        dataDict[col] = pointer
        return self._insert(dataDict)
