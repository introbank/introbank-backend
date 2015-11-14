# -*- coding: utf-8 -*-
from base_target_data_object import BaseTargetDataObject

class GroupDataObject(BaseTargetDataObject):
    tableName = "Group"

    def getInfoListToInsertMedia(self):
        infoList = []
        response = self._select(queryDict={"keys":"twitterId,album,hashtag"})
        try:
            for data in response["results"]:
                infoList.append({"objectId": data["objectId"], "twitterId":data["twitterId"],  "album":data["twitterId"], "hashtag":data["hashtag"]})
        except KeyError:
            raise Exception(response)

        return infoList

    @classmethod
    def cleanupHashtag(cls, hashtag):
        ## clean "#" at first
        return "#{0}".format(hashtag.replace("#", ''))

