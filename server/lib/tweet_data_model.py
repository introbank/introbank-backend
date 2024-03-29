# -*- coding: utf-8 -*-
from base_data_model import BaseDataModel, DataModelException
from tweet_data_object import TweetDataObject

class TweetDataModel(BaseDataModel):

    def saveTweetData(self, twitterId, twitterStatusId, text, className, objectId):
        try:
            ## connect
            self._connect()

            ## save media
            tweetDataObject = TweetDataObject(self.connection)
            res = tweetDataObject.save(twitterId, twitterStatusId, text, className, objectId)
            self.infoLog("save tweetData {0}".format(str(res)))

            ## close
            self._close()
            return res["objectId"]
        except KeyError:
            message = "unknown twitterid::".format(twitterId)
            self.warnLog(message)
            raise DataModelException(message)
