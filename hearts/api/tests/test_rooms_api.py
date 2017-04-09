from bson.objectid import ObjectId

from tests.utils import json_data


def test_create_room(api_client, db):
    response = json_data(api_client.post('/rooms/'))
    assert response['url']
    room_id = ObjectId(response['id'])
    cursor = db.rooms.find({"_id": room_id})
    assert cursor.count() == 1
    assert cursor[0]['users'] == []

    response = api_client.get(response['url'])
    assert response.status_code == 200
    assert response.content_type.startswith('text/html')


def test_join_room(api_client, socket_client, db):
    response = json_data(api_client.post('/rooms/'))
    room_id = response['id']
    socket_client.emit('join', {'room': room_id, 'username': 'wat'})

    received = socket_client.get_received()
    assert len(received) == 1
    assert len(received[0]['args']) == 1
    assert received[0]['args'][0] == 'wat has entered the room.'
