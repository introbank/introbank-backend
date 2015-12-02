# -*- coding: utf-8 -*-
from base_data_model import BaseDataModel, DataModelException
from media_data_object import MediaDataObject
from album_media_map_data_object import AlbumMediaMapDataObject

class MediaDataModel(BaseDataModel):

    def insertNewMedia(self, albumIds, twitterId, twitterStatusId, mediaUri, tweetObjectId):
        try:

            ## connect
            self._connect()

            ## insert media
            mediaDataObject = MediaDataObject(self.connection)
            res = mediaDataObject.insert(twitterId, twitterStatusId, mediaUri, tweetObjectId)
            print res
            print "== insert media =="
            mediaId = res["objectId"]

            ## insert AlbumMediaMap
            albumMediaMapDataObject = AlbumMediaMapDataObject(self.connection)
            for albumId in albumIds:
                albumMediaMapDataObject.insert(albumId, mediaId)
                print "== insert mediamap done =="

            ## close
            self._close()
        except KeyError:
            raise DataModelException("unknown twitterid::".format(twitterId))
