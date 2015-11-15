# -*- coding: utf-8 -*-
from base_data_model import BaseDataModel, DataModelException
from tweet_data_object import TweetDataObject

class TweetDataModel(BaseDataModel):

    def insertTweetData(self, twitterId, twitterStatusId, text, className, objectId):
        try:
            ## connect
            self._connect()

            ## insert media
            tweetDataObject = TweetDataObject(self.connection)
            res = tweetDataObject.insert(twitterId, twitterStatusId, text, className, objectId)
            print "== insert tweetData =="

            ## close
            self._close()
            return res["objectId"]
        except KeyError:
            raise DataModelException("unknown twitterid::".format(twitterId))
