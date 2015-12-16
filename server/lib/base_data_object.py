# -*- coding: utf-8 -*-
from logger_util import LoggerUtil
from abc import abstractmethod

class BaseDataObject(object):
    def __init__(self, connection, logger = LoggerUtil.getFileLogger()):
        self.logger = logger
        self.connection = connection
        self.className = self.getClassName()

    def _find(self, objectId = None, queryDict = []):
        return self.connection.find(self.className, objectId, queryDict)

    def _save(self, dataDict):
        return self.connection.save(self.className, dataDict)

    def infoLog(self, mesasge):
        self.logger.info(mesasge)

    def errorLog(self, message):
        self.logger.error(message)

    def warnLog(self, message):
        self.logger.warn(message)

    def debugLog(self, message):
        self.logger.debug(message)

    @abstractmethod
    def getClassName():
        pass

class DataObjectException(BaseException):
    pass
