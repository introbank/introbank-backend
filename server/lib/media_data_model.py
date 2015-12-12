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
            print res
            print "== save media =="
            mediaId = res["objectId"]

            ## save AlbumMediaMap
            albumMediaMapDataObject = AlbumMediaMapDataObject(self.connection)
            for albumId in albumIds:
                albumMediaMapDataObject.save(albumId, mediaId)
                print "== save mediamap done =="

            ## close
            self._close()
        except KeyError:
            raise DataModelException("unknown twitterid::".format(twitterId))
