#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import threading
import time
sys.path.append('{0}/../script'.format(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('{0}/../lib'.format(os.path.dirname(os.path.abspath(__file__))))
from twitter_data_streaming import TwitterDataStreaming
from base_executer import BaseExecuter
from logger_util import LoggerUtil

class TwitterDataStreamingDaemon(BaseExecuter):
    def __init__(self, minutes, isDaemon = False, logger = LoggerUtil.getFileLogger()):
        BaseExecuter.__init__(self, logger)
        self.minutes = int(minutes)
        self.thread = threading.Thread(name=self.__class__.__name__, target=self.proc)
        self.thread.setDaemon(isDaemon)

    def start(self):
        self.infoLog("TwitterDataStreamingDaemon start") 
        self.infoLog("interval::{0}min".format(self.minutes))
        self.thread.start()

    def proc(self):
        sec = 60 * self.minutes
        while True:
            streaming = TwitterDataStreaming()
            self.infoLog("main proc start")
            streaming.setup()    
            streaming.start()
            self.infoLog("sleep {0}sec".format(str(sec)))
            time.sleep(sec)
            streaming.stop()
        
if __name__ == '__main__':
    args = sys.argv
    interval = 0
    isDaemon = False
    if len(args) == 2:
        interval = args[1]
    elif(args) == 3:
        interval = args[1]
        isDaemon = True
    else:
        print "error:: 1st arg: interval(minutes), 2nd: debug"
        exit(1)

    daemon = TwitterDataStreamingDaemon(interval, isDaemon)
    daemon.start()
