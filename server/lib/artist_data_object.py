# -*- coding: utf-8 -*-
from base_target_data_object import BaseTargetDataObject

class ArtistDataObject(BaseTargetDataObject):
    tableName = "Artist"

    def getInfoToTwitterStream(self):
        infoList = []
        response = self._find(queryDict={"keys":"twitterId,album"})
        try:
            for data in response["results"]:
                infoList.append({"objectId": data["objectId"], "twitterId":data["twitterId"],  "album":data["album"]["objectId"]})
        except KeyError:
            raise Exception(response)

        return infoList


