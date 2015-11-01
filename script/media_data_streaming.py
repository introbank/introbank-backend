# -*- coding: utf-8 -*-
import sys, os 
sys.path.append('{0}/../lib'.format(os.path.dirname(os.path.abspath(__file__))))
from twitter_stream import TwitterStream
from media_data import MediaTableData

class MediaDataStreaming(object):
    def __init__(self):
        self.track = []
        self.follow = []

    def setTrack(self, track):
        self.track = track 
    
    def setFollow(self, follow):
        self.follow = follow

    def main(self):
        for item in TwitterStream.get(follow=self.follow, track=self.track):
            try:
                mediaList = item["entities"]["media"]
                text = item["text"]
                print "========="
                for media in mediaList:
                    data = MediaTableData(media['source_user_id'], media['source_status_id_str'], media['media_url'], text)
                    res = data.insert()
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
    streaming.setTrack(["#cheerz", "#idol"])
    streaming.main()
