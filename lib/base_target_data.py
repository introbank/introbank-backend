# -*- coding: utf-8 -*-
from twitter_util import TwitterUtil
from parse_connection import ParseConnection

class BaseTargetData(object):
    @classmethod
    def select(cls, objectId = None, queryDict = []):
        connection = ParseConnection()
        connection.connect()
        connection.select(cls.tableName, objectId, queryDict)

    @classmethod
    def getAllTwitterIdWithHash(cls):
        cls.select(queryDict={"keys":"twitterId,hashtag"})
