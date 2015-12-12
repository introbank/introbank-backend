# -*- coding: utf-8 -*-
from base_target_data_object import BaseTargetDataObject

class GroupDataObject(BaseTargetDataObject):
    tableName = "Group"

    def getInfoToTwitterStream(self):
        infoList = []
        response = self._find(queryDict={"keys":"twitterId,album,hashtag,subTwitterIds"})
        try:
            for data in response["results"]:
                info = {"objectId": data["objectId"], "twitterId":data["twitterId"],  "album":data["album"]["objectId"], "hashtag":GroupDataObject.cleanupHashtag(data["hashtag"]), "subTwitterIds": []}
                if "subTwitterIds" in data.keys():
                    info["subTwitterIds"] = data["subTwitterIds"]

                infoList.append(info)
        except KeyError as e:
            raise Exception(e)

        return infoList

    @classmethod
    def cleanupHashtag(cls, hashtag):
        ## clean "#" at first
        hashtag = hashtag.encode("utf-8")
        return "#{0}".format(hashtag.replace("#", ''))


