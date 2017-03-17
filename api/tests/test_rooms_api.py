from bson.objectid import ObjectId

from tests.utils import json_data


def test_create_room(api, db):
    response = json_data(api.post('/rooms/'))
    assert response['url']
    room_id = ObjectId(response['id'])
    cursor = db.rooms.find({"_id": room_id})
    assert cursor.count() == 1
