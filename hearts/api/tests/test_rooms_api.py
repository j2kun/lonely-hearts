from bson.objectid import ObjectId

from tests.utils import json_data


def test_create_room(api, db):
    response = json_data(api.post('/rooms/'))
    assert response['url']
    room_id = ObjectId(response['id'])
    cursor = db.rooms.find({"_id": room_id})
    assert cursor.count() == 1

    response = api.get(response['url'])
    assert response.status_code == 200
    assert response.content_type.startswith('text/html')
