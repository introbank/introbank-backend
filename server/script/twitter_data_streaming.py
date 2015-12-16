#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os 
import threading
sys.path.append('{0}/../lib'.format(os.path.dirname(os.path.abspath(__file__))))
from logger_util import LoggerUtil
from twitter_stream import TwitterStream
from artist_data_object import ArtistDataObject
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

    def __init__(self, logger = LoggerUtil.getFileLogger()):
        self.connection = ParseConnection()
        self.logger = logger
        self.track = []
        self.follow = []
        self.twitterIdInfo = {}
        self.hashtagAlbumIdMap = {}
        self.running = threading.Event()
        self.thread = threading.Thread(target = self.main)

    def infoLog(self, message):
        LoggerUtil.encodedLog(self.logger.info, message)

    def errorLog(self, message):
        LoggerUtil.encodedLog(self.logger.error, message)

    def warnLog(self, message):
        LoggerUtil.encodedLog(self.logger.warn, message)

    def debugLog(self, message):
        LoggerUtil.encodedLog(self.logger.debug, message)

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
    
    def getAlbumIdList(self, twitterId = None, hashtags = []):
        albumIdList = [] 
        if self.twitterId2AlbumId(twitterId) is not None:
            albumIdList.append(self.twitterId2AlbumId(twitterId))

        for hashtagInfo in hashtags:
            hashtag = "#" + hashtagInfo["text"]
            if self.hashtag2AlbumId(hashtag) is not None:
                albumIdList.append(self.hashtag2AlbumId(hashtag))

        return albumIdList

    def setup(self):
        print "setup start"
        self.infoLog("set up start")
        ## data from DB
        artistDataObject = ArtistDataObject(self.connection)
        groupDataObject = GroupDataObject(self.connection)

        ## start 
        self.connection.connect()
        artistData = artistDataObject.getInfoToTwitterStream()
        groupData = groupDataObject.getInfoToTwitterStream()
        self.connection.close()
        ## end

        for artist in artistData:
            self.follow.append(artist["twitterId"])
            self.twitterIdInfo[artist["twitterId"]] = {"albumId":artist["album"], "classInfo":ParseClassInfo("Artist", artist["objectId"])}

        for group in groupData:
            self.follow.append(group["twitterId"])
            self.twitterIdInfo[group["twitterId"]] = {"albumId":group["album"], "classInfo":ParseClassInfo("Group", group["objectId"])}

            if (group["hashtag"] is not None):
                self.track.append(group["hashtag"])
                self.hashtagAlbumIdMap[group["hashtag"]] = group["album"]

            
            # add subTwitterIds
            for subTwitterId in group["subTwitterIds"]:
                self.follow.append(subTwitterId)
                self.twitterIdInfo[subTwitterId] = {"albumId":group["album"], "classInfo":ParseClassInfo("Group", group["objectId"])}

        self.infoLog("follow::" + ",".join(self.follow))
#        self.infoLog("track::" + ",".join(self.track))




    def main(self):
        print "main start"
        self.infoLog("main start")
        for item in TwitterStream.get(follow=self.follow, track=self.track):
            ## save TweetId
            try:
                twitterId = item["user"]["id_str"] 
                twitterStatusId = item["id_str"]
                text = item["text"]

                classInfo = self.getClassInfo(twitterId)

                if classInfo is not None:
                    print "::" + twitterId + "::" + twitterStatusId + "::" + text
                    ## save tweet
                    tweetDataModel = TweetDataModel(self.connection)
                    tweetObjectId = tweetDataModel.saveTweetData(twitterId, twitterStatusId, text, classInfo.name, classInfo.objectId)
                    ## save Album
                    mediaList = item["extended_entities"]["media"]
                    hashtags = item["entities"]["hashtags"]
                    for media in mediaList:
                        mediaDataModel = MediaDataModel(self.connection)
                        
                        albumIds = self.getAlbumIdList(twitterId, hashtags)
                        if len(albumIds) > 0:
                            mediaDataModel.saveNewMedia(albumIds, twitterId, twitterStatusId, media['media_url_https'], tweetObjectId)

            except (KeyError, BrankMediaData) as e:
                self.errorLog(e)
        
            if not self.isRunning():
                print "stop main steraming"
                exit(0)

    def isRunning(self):
        return self.running.isSet()

    def start(self):
        if self.check():
            print "already proc running"
            exit(1)

        print "start main streaming proc..."
        self.running.set()
        self.thread.start()

    def stop(self):
        self.running.clear()
        print "stop main steraming proc..."
        self.thread.join()

    def check(self):
        if self.thread.isAlive():
            print "main steraming proc is alive"
            return True
        else:
            print "main steraming proc is not alive"
            return False

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
