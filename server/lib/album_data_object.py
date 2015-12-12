# -*- coding: utf-8 -*-
from base_data_object import BaseDataObject

class AlbumDataObject(BaseDataObject):
    tableName = "Album"

    def save(self, album, media, isViewable = True):
        isViewableStr = self.getIsViewableString(isViewable)
        objects = [{"__type": "Pointer", "className":"Album", "objectId":album}
                , {"__type": "Pointer", "className":"Media", "objectId":media}]

        opponents = {"__op": "AddRelation", "objects": objects}
        dataDict = {"opponents": opponents, "isViewable": isViewableStr}
        return self._save(dataDict)

    @classmethod
    def getIsViewableString(cls, isViewable):
        return "true" if isViewable else "false"

