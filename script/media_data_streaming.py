# -*- coding: utf-8 -*-
import sys, os 
sys.path.append('{0}/../lib'.format(os.path.dirname(os.path.abspath(__file__))))
from twitter_stream import TwitterStream
from performer_data_object import PerformerDataObject
from group_data_object import GroupDataObject
from media_data_model import MediaDataModel
from parse_connection import ParseConnection

class MediaDataStreaming(object):
    COMMIN_TRACK = ["#ƒAƒCƒhƒ‹"]

    def __init__(self):
        self.connection = ParseConnection()
        self.track = []
        self.follow = []
        self.twitterAlbumIdMap = {}
        self.hashtagAlbumIdMap = {}

    def twitterId2AlbumId(self, twitterId):
        try:
            return self.twitterAlbumIdMap[twitterId]
        except KeyError:
            return None

    def hashtag2AlbumId(self, hashtag):
        try:
            return self.hashtagAlbumIdMap[hashtag]
        except KeyError:
            return None
    
    def getAlbumIdList(self, twitterId = None, hashtag = None):
        albumIdList = [] 
        if self.twitterId2AlbumId(twitterId) is not None:
            albumIdList.append(self.twitterId2AlbumId(twitterId))

        if self.hashtag2AlbumId(twitterId) is not None:
            albumIdList.append(self.hashtag2AlbumId(twitterId))

        ## test
        if albumIdList == []:
            albumIdList.append("WCPy9Wi9IK")

        ##
        return albumIdList

    def setup(self):
        ## data from DB
        performerDataObject = PerformerDataObject(self.connection)
        groupDataObject = GroupDataObject(self.connection)

        ## start 
        self.connection.connect()
        performerData = performerDataObject.getInfoListToInsertMedia()
        groupData = groupDataObject.getInfoListToInsertMedia()
        self.connection.close()
        ## end

        for performer in performerData:
            self.follow.append(performer["twitterId"])
            self.twitterAlbumIdMap["twitterId"] = performer["album"]

        for group in groupData:
            self.follow.append(group["twitterId"])
            self.track.append(group["hashtag"])

            ## test
            self.track.append("twitter")

            self.twitterAlbumIdMap["twitterId"] = group["album"]
            self.hashtagAlbumIdMap[group["hashtag"]] = group["album"]

        print "follow::" + ",".join(self.follow)
        print "track::" + ",".join(self.track)

    def start(self):
        print "start main streaming proc"
        for item in TwitterStream.get(follow=self.follow, track=self.track):
            try:
                mediaList = item["entities"]["media"]
                text = item["text"]
                print "========="
                for media in mediaList:
                    mediaDataModel = MediaDataModel(self.connection)
                    
                    for album in self.getAlbumIdList(media['source_user_id']):
                        res = mediaDataModel.insertNewMedia(album, media['source_user_id'], media['source_status_id_str'], media['media_url'], text)
                        print res
            except (KeyError, BrankMediaData):
                pass

    def _validate(cls, media):
        for key in ['source_user_id', 'source_status_id_str', 'media_url']:
            if media[key]:
                pass
            else:
                raise BrankMediaData

class BrankMediaData(BaseException):
    pass
        
if __name__ == '__main__':
    streaming = MediaDataStreaming()
    streaming.setup()    
    streaming.start()
