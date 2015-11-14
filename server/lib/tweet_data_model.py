# -*- coding: utf-8 -*-
from base_data_model import BaseDataModel, DataModelException
from tweet_data_object import TweetDataObject

class TweetDataModel(BaseDataModel):

    def insertTweetData(self, twitterId, twitterStatusId, className, objectId):
        try:
            ## connect
            self._connect()

            ## insert media
            tweetDataObject = TweetDataObject(self.connection)
            res = tweetDataObject.insert(twitterId, twitterStatusId, className, objectId)
            print "== insert tweetData =="
            print res

            ## close
            self._close()
        except KeyError:
            raise DataModelException("unknown twitterid::".format(twitterId))
