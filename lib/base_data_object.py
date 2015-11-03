# -*- coding: utf-8 -*-

class BaseDataObject(object):
    def __init__(self, connection):
        self.connection = connection

    def _select(self, objectId = None, queryDict = []):
        return self.connection.select(self.tableName, objectId, queryDict)

    def _insert(self, dataDict):
        return self.connection.insert(self.tableName, dataDict)

class DataObjectException(BaseException):
    pass
