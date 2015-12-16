# -*- coding: utf-8 -*-
from logger_util import LoggerUtil

class BaseDataModel(object):
    def __init__(self, connection, logger = LoggerUtil.getFileLogger()):
        self.connection = connection
        self.logger = logger

    def _connect(self):
        self.connection.connect()

    def _close(self):
        self.connection.close()

    def infoLog(self, message):
        LoggerUtil.encodedLog(self.logger.info, message)

    def errorLog(self, message):
        LoggerUtil.encodedLog(self.logger.error, message)

    def warnLog(self, message):
        LoggerUtil.encodedLog(self.logger.warn, message)

    def debugLog(self, message):
        LoggerUtil.encodedLog(self.logger.debug, message)


class DataModelException(BaseException):
    pass
