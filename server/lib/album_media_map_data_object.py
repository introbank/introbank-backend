# -*- coding: utf-8 -*-
from base_data_object import BaseDataObject

class AlbumMediaMapDataObject(BaseDataObject):
    tableName = "AlbumMediaMap"

    def insert(self, album, media, isViewable = True):
        isViewableStr = self.getIsViewableString(isViewable)
        objects = [{"__type": "Pointer", "className":"Album", "objectId":album}
                , {"__type": "Pointer", "className":"Media", "objectId":media}]

        opponents = {"__op": "AddRelation", "objects": objects}
        dataDict = {"opponents": opponents, "isViewable": isViewableStr}
        return self._insert(dataDict)

    @classmethod
    def getIsViewableString(cls, isViewable):
        return "true" if isViewable else "false"
