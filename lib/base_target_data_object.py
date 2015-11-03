# -*- coding: utf-8 -*-
from twitter_util import TwitterUtil
from parse_connection import ParseConnection
from base_data_object import BaseDataObject

class BaseTargetDataObject(BaseDataObject):
    @classmethod
    def getAllTwitterIdList(cls):
        objectIdList = []
        twitterIdList = []

        response = cls.select(queryDict={"keys":"twitterId"})
        try:
            for data in response["results"]:
                objectIdList.append(data["objectId"])
                twitterIdList.append(data["twitterId"])
        except KeyError as e:
            raise Exception(response)

        return {"objectIdList": objectIdList, "twitterIdList": twitterIdList}       

