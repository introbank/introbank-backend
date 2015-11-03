# -*- coding: utf-8 -*-
from abc import abstractmethod
from parse_connection import ParseConnection

class BaseDataObject(object):
    @classmethod
    def select(cls, objectId = None, queryDict = []):
        connection = ParseConnection()
        connection.connect()
        return connection.select(cls.tableName, objectId, queryDict)

#    @abstractmethod
#    def update(self):
#        pass
#
#    @abstractmethod
#    def select(self):
#        pass
