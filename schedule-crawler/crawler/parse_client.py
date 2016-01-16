import json
import httplib
import urllib


class ParseClient(object):

    @classmethod
    def insert_event(cls, item):
        if cls.is_existed(item):
            return

        connection = httplib.HTTPSConnection('api.parse.com', 443)
        connection.connect()
        connection.request('POST', '/1/classes/Event', json.dumps({
            "groups": {
                "__op": "AddRelation",
                "objects": [{
                    "__type": "Pointer",
                    "className": "Group",
                    "objectId": item['objectId']
                }]
            },
            "date": {
                "__type": "Date",
                "iso": item['date']
            },
            "title": item['title'],
            "detail": item['detail'],
            "place": item['place'],
            "charge": item['charge']
        }), {
            "X-Parse-Application-Id": "LID0MpbVk0JBivgVMSO6hXO5cQ3wBdlgvA8eEbES",
            "X-Parse-REST-API-Key": "NX4EsDtr6k1OsyN9BjBpHrJZUsZPUaaI1MO0Pzxm",
            "Content-Type": "application/json"
        })
        results = json.loads(connection.getresponse().read())
        print results

    @classmethod
    def is_existed(cls, item):
        connection = httplib.HTTPSConnection('api.parse.com', 443)
        params = urllib.urlencode({"where":json.dumps({
            "title": item['title'],
            "place": item['place'],
            "groups": {
                "__type": "Pointer",
                "className": "Group",
                "objectId": item['objectId']
            }
        })})
        connection.connect()
        connection.request('GET', '/1/classes/Event?%s' % params, '', {
            "X-Parse-Application-Id": "LID0MpbVk0JBivgVMSO6hXO5cQ3wBdlgvA8eEbES",
            "X-Parse-REST-API-Key": "NX4EsDtr6k1OsyN9BjBpHrJZUsZPUaaI1MO0Pzxm"
        })
        result = json.loads(connection.getresponse().read())
        if len(result['results']) > 0:
            return True
        else:
            return False
