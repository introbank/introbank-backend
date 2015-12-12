# -*- coding: utf-8 -*-

class BaseDataObject(object):
    def __init__(self, connection):
        self.connection = connection

    def _find(self, objectId = None, queryDict = []):
        return self.connection.find(self.tableName, objectId, queryDict)

    def _save(self, dataDict):
        return self.connection.save(self.tableName, dataDict)

class DataObjectException(BaseException):
    pass
