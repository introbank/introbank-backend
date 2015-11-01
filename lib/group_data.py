# -*- coding: utf-8 -*-
from twitter_util import TwitterUtil
from parse_connection import ParseConnection
from base_target_data import BaseTargetData

class GroupData(BaseTargetData):
    tableName = "Group"

    @classmethod
    def getAllTwitterIdListWithHashtagList(cls):
        twitterIdList = []
        hashtagList = []
        response = cls.select(queryDict={"keys":"twitterId,hashtag"})
        try:
            for data in response["results"]:
                twitterIdList.append(data["twitterId"])
                hashtagList.append(cls.cleanupHashtag(data["hashtag"]))
        except KeyError:
            raise Exception(response)

        return {"twitterIdList":twitterIdList, "hashtagList":hashtagList}

    @classmethod
    def cleanupHashtag(cls, hashtag):
        ## clean "#" at first
        return "#{0}".format(hashtag.replace("#", ''))

