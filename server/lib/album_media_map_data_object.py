# -*- coding: utf-8 -*-
from base_data_object import BaseDataObject

class AlbumMediaMapDataObject(BaseDataObject):
    tableName = "AlbumMediaMap"

    def insert(self, albumId, mediaId, isViewable = False):
        album = {"__type": "Pointer", "className":"Album", "objectId":albumId}
        media =  {"__type": "Pointer", "className":"Media", "objectId":mediaId}

        dataDict = {"album": album, "media":media, "isViewable": isViewable}
        res = self._insert(dataDict)
        print res
        return res

