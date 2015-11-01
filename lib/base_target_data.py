# -*- coding: utf-8 -*-
from twitter_util import TwitterUtil
from parse_connection import ParseConnection

class BaseTargetData(object):
    @classmethod
    def select(cls, objectId = None, queryDict = []):
        connection = ParseConnection()
        connection.connect()
        return connection.select(cls.tableName, objectId, queryDict)

    @classmethod
    def getAllTwitterIdList(cls):
        twitterIdList = []
        response = cls.select(queryDict={"keys":"twitterId"})
        try:
            for data in response["results"]:
                twitterIdList.append(data["twitterId"])
        except KeyError as e:
            raise Exception(response)

        return twitterIdList       

