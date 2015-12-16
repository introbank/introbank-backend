# -*- coding: utf-8 -*-
from base_data_model import BaseDataModel, DataModelException
from media_data_object import MediaDataObject
from album_media_map_data_object import AlbumMediaMapDataObject

class MediaDataModel(BaseDataModel):

    def saveNewMedia(self, albumIds, twitterId, twitterStatusId, mediaUri, tweetObjectId):
        try:

            ## connect
            self._connect()

            ## save media
            mediaDataObject = MediaDataObject(self.connection)
            res = mediaDataObject.save(twitterId, twitterStatusId, mediaUri, tweetObjectId)
            self.infoLog("save media::{0}".format(str(res)))
            mediaId = res["objectId"]

            ## save AlbumMediaMap
            albumMediaMapDataObject = AlbumMediaMapDataObject(self.connection)
            for albumId in albumIds:
                res = albumMediaMapDataObject.save(albumId, mediaId)
                self.infoLog("save media map::{0}".format(str(res)))
                self.infoLog("save media & map succeed")

            ## close
            self._close()
        except KeyError:
            message = "unknown twitterid::".format(twitterId)
            self.warnLog(message)
            raise DataModelException(message)
