#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
import logging
import logging.config

class LoggerUtil(object):
    CONFIG = '{0}/../config/logger_conf.yaml'.format(os.path.dirname(os.path.abspath(__file__)))

    @classmethod
    def _getLogger(cls, loggerType):
        try:
            with open(cls.CONFIG) as f:
                configDir = yaml.load(f)
            
            logging.config.dictConfig(configDir)
            return logging.getLogger(loggerType)
        except Exception as e:
            raise LogUtilException(e)

    @classmethod
    def getFileLogger(cls):
        try:
            return cls._getLogger('file')
        except Exception as e:
            raise LogUtilException(e)
        
    @classmethod
    def getConsoleLogger(cls):
        try:
            return cls._getLogger('console')
        except Exception as e:
            raise LogUtilException(e)

class LogUtilException(BaseException):
    pass
