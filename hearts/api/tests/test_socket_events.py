from tests.utils import json_data


def test_db(api_client, db):
    assert db.rooms.find({}).count() == 0


def test_on_join_valid_room(api_client, socket_client, db):
    db.rooms.insert_one({'room_id': '12345', 'users': []})   # set up the room document
    socket_client.emit('join', {'room': db.rooms['room_id'], 'username': 'wat'})  # should it be socket_client or api_client?
    pass


def test_on_join_invald_room(api_client, db):
    pass
