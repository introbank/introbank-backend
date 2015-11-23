#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import threading
import time
sys.path.append('{0}/../script'.format(os.path.dirname(os.path.abspath(__file__))))
from twitter_data_streaming import TwitterDataStreaming

class TwitterDataStreamingDaemon(object):
    def __init__(self, minutes, debugMode = False):
       self.minutes = int(minutes)
       self.thread = threading.Thread(name=self.__class__.__name__, target=self.proc) 
       if debugMode is False:
           self.thread.setDaemon(True)

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
            time.sleep(sec)
            streaming.stop()
        
if __name__ == '__main__':
    args = sys.argv
    interval = 0
    debugMode = False
    if len(args) == 2:
        interval = args[1]
    elif len(args) == 3:
        interval = args[1]
        debugMode = True
    else:
        print "error:: 1st arg: interval(minutes), 2nd: debug"
        exit(1)

    daemon = TwitterDataStreamingDaemon(interval, debugMode)
    daemon.start()
