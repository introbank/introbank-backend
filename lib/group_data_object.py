# -*- coding: utf-8 -*-
from twitter_util import TwitterUtil
from parse_connection import ParseConnection
from base_target_data_object import BaseTargetDataObject

class GroupDataObject(BaseTargetDataObject):
    tableName = "Group"

    @classmethod
    def getAllTwitterIdListWithHashtagList(cls):
        objectIdList = []
        twitterIdList = []
        hashtagList = []
        response = cls.select(queryDict={"keys":"twitterId,hashtag"})
        try:
            for data in response["results"]:
                objectIdList.append(data["objectId"])
                twitterIdList.append(data["twitterId"])
                hashtagList.append(cls.cleanupHashtag(data["hashtag"]))
        except KeyError:
            raise Exception(response)

        return {"objectIdList": objectIdList, "twitterIdList":twitterIdList, "hashtagList":hashtagList}

    @classmethod
    def cleanupHashtag(cls, hashtag):
        ## clean "#" at first
        return "#{0}".format(hashtag.replace("#", ''))

