# -*- coding: utf-8 -*-
from abc import abstractmethod
from parse_connection import ParseConnection

class BaseTable(object):

    @abstractmethod
    def insert(self):
        pass

#    @abstractmethod
#    def update(self):
#        pass
#
#    @abstractmethod
#    def select(self):
#        pass
