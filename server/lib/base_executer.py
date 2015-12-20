#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logger_util import LoggerUtil

class BaseExecuter(object):
    def __init__(self, logger = LoggerUtil.getFileLogger()):
        self.logger = logger

    def infoLog(self, message):
        LoggerUtil.encodedLog(self.logger.info, message)

    def errorLog(self, message):
        LoggerUtil.encodedLog(self.logger.error, message)

    def warnLog(self, message):
        LoggerUtil.encodedLog(self.logger.warn, message)

    def debugLog(self, message):
        LoggerUtil.encodedLog(self.logger.debug, message)

class ExecuterException(BaseException):
    pass
