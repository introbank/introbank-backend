# -*- coding: utf-8 -*-
from base_target_data_object import BaseTargetDataObject

class PerformerDataObject(BaseTargetDataObject):
    tableName = "Performer"

    def getInfoListToInsertMedia(self):
        infoList = []
        response = self._select(queryDict={"keys":"twitterId,album"})
        try:
            for data in response["results"]:
                infoList.append({"objectId": data["objectId"], "twitterId":data["twitterId"],  "album":data["twitterId"]})
        except KeyError:
            raise Exception(response)

        return infoList


