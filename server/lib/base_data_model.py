# -*- coding: utf-8 -*-

class BaseDataModel(object):
    def __init__(self, connection):
        self.connection = connection

    def _connect(self):
        self.connection.connect()

    def _close(self):
        self.connection.close()

class DataModelException(BaseException):
    pass
