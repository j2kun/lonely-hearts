from tests.utils import json_data


def test_create_room(api_client, db):
    response = json_data(api_client.post('/rooms/'))
    assert response['url']
    room_id = response['url'].split('/')[2]
    assert room_id
    response = api_client.get(response['url'])
    assert response.status_code == 200
    assert response.content_type.startswith('text/html')


def test_join_room(api_client, socket_client, db):
    response = json_data(api_client.post('/rooms/'))
    room_id = response['url'].split('/')[2]
    socket_client.emit('join', {'room': room_id, 'username': 'wat'})

    received = socket_client.get_received()
    assert len(received) == 1
    assert len(received[0]['args']) == 1
    assert received[0]['args'][0] == 'wat has entered the room.'
