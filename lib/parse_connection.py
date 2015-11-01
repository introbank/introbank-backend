# -*- coding: utf-8 -*-

import json
import httplib
import urllib

class ParseConnection(object):
    URL = 'api.parse.com'
    PORT = 443
    META_DATA = {
       "X-Parse-Application-Id": "LID0MpbVk0JBivgVMSO6hXO5cQ3wBdlgvA8eEbES",
       "X-Parse-REST-API-Key": "NX4EsDtr6k1OsyN9BjBpHrJZUsZPUaaI1MO0Pzxm",
       "Content-Type": "application/json"
    } 

    def __init__(self):
        self.connection = httplib.HTTPSConnection(self.URL, self.PORT)

    def connect(self):
        self.connection.connect()

    def insert(self, table, dataDict):
        self.connection.request('POST', '/1/classes/{0}'.format(table), json.dumps(dataDict), self.META_DATA)
        return json.loads(self.connection.getresponse().read())

    def select(self, table, objectId = None, queryDict = []):
        path =  "" if objectId == None else "/{0}".format(objectId)
        query = "" if queryDict == [] else "?{0}".format(urllib.urlencode(queryDict))
        url = '/1/classes/{0}{1}{2}'.format(table, path, query)
        print url
        self.connection.request('GET', url, '', self.META_DATA)
        res = json.loads(self.connection.getresponse().read())
        print res
        return res
