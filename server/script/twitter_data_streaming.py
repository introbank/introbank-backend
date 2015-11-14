# -*- coding: utf-8 -*-
import sys, os 
sys.path.append('{0}/../lib'.format(os.path.dirname(os.path.abspath(__file__))))
from twitter_stream import TwitterStream
from performer_data_object import PerformerDataObject
from group_data_object import GroupDataObject
from media_data_model import MediaDataModel
from tweet_data_model import TweetDataModel
from parse_connection import ParseConnection

class ParseClassInfo(object):
    def __init__(self, name, objectId):
        self.name = name
        self.objectId = objectId

class TwitterDataStreaming(object):
    COMMIN_TRACK = ["#ƒAƒCƒhƒ‹"]

    def __init__(self):
        self.connection = ParseConnection()
        self.track = []
        self.follow = []
        self.twitterIdInfo = {}
        self.hashtagAlbumIdMap = {}

    def twitterId2AlbumId(self, twitterId):
        try:
            return self.twitterIdInfo[twitterId]["albumId"]
        except KeyError:
            return None

    def getClassInfo(self, twitterId):
        try:
            classInfo = self.twitterIdInfo[twitterId]["classInfo"]
            return classInfo
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

        return albumIdList

    def setup(self):
        ## data from DB
        performerDataObject = PerformerDataObject(self.connection)
        groupDataObject = GroupDataObject(self.connection)

        ## start 
        self.connection.connect()
        performerData = performerDataObject.getInfoToTwitterStream()
        groupData = groupDataObject.getInfoToTwitterStream()
        self.connection.close()
        ## end

        for performer in performerData:
            self.follow.append(performer["twitterId"])
            self.twitterIdInfo[performer["twitterId"]] = {"albumId":performer["album"], "classInfo":ParseClassInfo("Performer", performer["objectId"])}

        for group in groupData:
            self.follow.append(group["twitterId"])
            self.track.append(group["hashtag"])
            self.twitterIdInfo[group["twitterId"]] = {"albumId":group["album"], "classInfo":ParseClassInfo("Group", group["objectId"])}
            self.hashtagAlbumIdMap[group["hashtag"]] = group["album"]


        print "follow::" + ",".join(self.follow)
        print "track::" + ",".join(self.track)
        print self.twitterIdInfo

    def start(self):
        print "start main streaming proc"
        for item in TwitterStream.get(follow=self.follow, track=self.track):
            ## insert TweetId
            try:
                twitterId = item["user"]["id_str"] 
                twitterStatusId = item["id_str"]
                text = item["text"]

                classInfo = self.getClassInfo(twitterId)

                if classInfo is not None:
                    print "::" + twitterId + "::" + twitterStatusId + "::" + text
                    tweetDataModel = TweetDataModel(self.connection)
                    tweetDataModel.insertTweetData(twitterId, twitterStatusId, classInfo.name, classInfo.objectId)
            except Exception as e:
                pass
            ## insert Album
            try:
                mediaList = item["entities"]["media"]
                for media in mediaList:
                    print media
                    mediaDataModel = MediaDataModel(self.connection)
                    
                    for album in self.getAlbumIdList(twitterId):
                        res = mediaDataModel.insertNewMedia(album, twitterId, twitterStatusId, media['media_url_https'], text)
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
    streaming = TwitterDataStreaming()
    streaming.setup()    
    streaming.start()
