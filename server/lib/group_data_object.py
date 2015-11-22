# -*- coding: utf-8 -*-
from base_target_data_object import BaseTargetDataObject

class GroupDataObject(BaseTargetDataObject):
    tableName = "Group"

    def getInfoToTwitterStream(self):
        infoList = []
        response = self._select(queryDict={"keys":"twitterId,album,hashtag"})
        try:
            for data in response["results"]:
                infoList.append({"objectId": data["objectId"], "twitterId":data["twitterId"],  "album":data["album"]["objectId"], "hashtag":GroupDataObject.cleanupHashtag(data["hashtag"])})
        except KeyError as e:
            raise Exception(e)

        return infoList

    @classmethod
    def cleanupHashtag(cls, hashtag):
        ## clean "#" at first
        return "#{0}".format(hashtag.replace("#", ''))


