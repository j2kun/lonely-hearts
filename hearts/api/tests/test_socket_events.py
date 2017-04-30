from hearts.api.rooms import create_room
from hearts.api.rooms import get_room


def test_db(db):
    assert db.rooms.find({}).count() == 0


def test_create_room(db):
    test_room = create_room()
    assert test_room['users'] == []
    test_room2 = create_room(('Daniel', 'Lauren', 'Erin', 'Jeremy'))
    assert test_room2['users'] == ['Daniel', 'Lauren', 'Erin', 'Jeremy']


def test_on_join_valid_room(api_client, socket_client, db):
    test_room = create_room()
    test_room_id = str(test_room['_id'])

    socket_client.emit('join', {'room': test_room_id, 'username': 'user_1'})

    test_room = get_room(test_room_id)
    assert test_room['users'] == ['user_1']

    socket_client.emit('join', {'room': test_room_id, 'username': 'user_2'})
    socket_client.emit('join', {'room': test_room_id, 'username': 'user_3'})
    socket_client.emit('join', {'room': test_room_id, 'username': 'user_4'})
    test_room = get_room(test_room_id)
    assert set(test_room['users']) == {'user_1', 'user_2', 'user_3', 'user_4'}


def test_is_room_full(db):
    assert False


def test_create_game_write_to_database(db):
    assert False


def test_create_game_when_room_is_not_full(db):
    assert False


def test_create_game_when_room_is_full(db):
    assert False
