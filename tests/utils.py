import json


def json_data(response):
    return json.loads(response.data.decode('utf-8'))
