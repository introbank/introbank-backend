# -*- coding: utf-8 -*-
from base_target_data_object import BaseTargetDataObject

class ArtistDataObject(BaseTargetDataObject):
    @classmethod
    def getClassName(cls):
        return "Artist"

    def getInfoToTwitterStream(self):
        infoList = []
        response = self._find(queryDict={"keys":"twitterId,album"})
        try:
            for data in response["results"]:
                objectId = data["objectId"]
                infoList.append({"objectId": objectId, "twitterId":data["twitterId"],  "album":data["album"]["objectId"]})
        except KeyError as e:
            self.errorLog("artist objectId={0} has error.".format(objectId))
            raise Exception(e)

        return infoList


