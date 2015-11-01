# -*- coding: utf-8 -*-
import sys, os 
sys.path.append('{0}/../lib'.format(os.path.dirname(os.path.abspath(__file__))))
from twitter_stream import TwitterStream
from media_data import MediaTableData
from performer_data import PerformerData
from group_data import GroupData

class MediaDataStreaming(object):
    COMMIN_TRACK = ["#ƒAƒCƒhƒ‹"]

    def __init__(self):
        self.track = []
        self.follow = []

    def setTrack(self, track):
        self.track = track 
    
    def setFollow(self, follow):
        self.follow = follow

    def main(self):
        print "start main streaming proc"
        for item in TwitterStream.get(follow=self.follow, track=self.track):
            try:
                mediaList = item["entities"]["media"]
                text = item["text"]
                print "========="
                for media in mediaList:
                    data = MediaTableData()
                    res = data.insert(media['source_user_id'], media['source_status_id_str'], media['media_url'], text)
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
    performer = PerformerData()
    group = GroupData()
    
    follow = []
    track = []

    follow += performer.getAllTwitterIdList()
    followWithTrack = group.getAllTwitterIdListWithHashtagList()
    
    follow += followWithTrack["twitterIdList"]
    track += followWithTrack["hashtagList"]
    
    print follow
    print track

    streaming.setFollow(follow)
    streaming.setTrack(track)
    streaming.main()
