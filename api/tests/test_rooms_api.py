from tests.utils import json_data


def test_create_room(api, db):
    response = json_data(api.post('/rooms/'))
    assert response['url']
    cursor = db.rooms.find({"id": response['room_id']})
    assert cursor.count() == 1
