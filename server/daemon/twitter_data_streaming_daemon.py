#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import threading
import time
sys.path.append('{0}/../script'.format(os.path.dirname(os.path.abspath(__file__))))
from twitter_data_streaming import TwitterDataStreaming

class TwitterDataStreamingDaemon(object):
    def __init__(self, minutes):
       self.minutes = int(minutes)
       self.thread = threading.Thread(name=self.__class__.__name__, target=self.proc) 

    def start(self):
        print "TwitterDataStreamingDaemon start"
        print "interval::{0}min".format(self.minutes)
        self.thread.start()

    def proc(self):
        sec = 60 * self.minutes
        while True:
            streaming = TwitterDataStreaming()
            print "main proc"
            streaming.setup()    
            streaming.start()
            print "sleep {0}sec".format(str(sec))
            time.sleep(sec)
            streaming.stop()
        
if __name__ == '__main__':
    args = sys.argv
    interval = 0
    if len(args) == 2:
        interval = args[1]
    else:
        print "error:: 1st arg: interval(minutes), 2nd: debug"
        exit(1)

    daemon = TwitterDataStreamingDaemon(interval)
    daemon.start()
