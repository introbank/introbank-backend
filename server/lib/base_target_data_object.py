# -*- coding: utf-8 -*-
from base_data_object import BaseDataObject
from abc import abstractmethod

class BaseTargetDataObject(BaseDataObject):

    def getAllTwitterIdList(self):
        objectIdList = []
        twitterIdList = []

        response = self._select(queryDict={"keys":"twitterId"})
        try:
            for data in response["results"]:
                objectIdList.append(data["objectId"])
                twitterIdList.append(data["twitterId"])
        except KeyError:
            raise Exception(response)

        return {"objectIdList": objectIdList, "twitterIdList": twitterIdList}       

    @abstractmethod
    def getInfoToTwitterStream(self):
        pass
