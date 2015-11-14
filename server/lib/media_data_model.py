# -*- coding: utf-8 -*-
from base_data_model import BaseDataModel, DataModelException
from media_data_object import MediaDataObject
from album_media_map_data_object import AlbumMediaMapDataObject

class MediaDataModel(BaseDataModel):

    def insertNewMedia(self, albumId, twitterId, twitterStatusId, mediaUri, info, hashtag = None):
        try:

            ## connect
            self._connect()

            ## insert media
            mediaDataObject = MediaDataObject(self.connection)
            res = mediaDataObject.insert(twitterId, twitterStatusId, mediaUri, info, hashtag)
            print "== insert media =="
            print res
            mediaId = res["objectId"]

            ## insert AlbumMediaMap
            albumMediaMapDataObject = AlbumMediaMapDataObject(self.connection)
            albumMediaMapDataObject.insert(albumId, mediaId)
            print "== insert done =="

            ## close
            self._close()
        except KeyError:
            raise DataModelException("unknown twitterid::".format(twitterId))
