from hearts.api.rooms import create_room


def test_db(db):
    assert db.rooms.find({}).count() == 0


def test_create_room(db):
    test_room = create_room()
    assert test_room['users'] == []


def test_on_join_valid_room(api_client, socket_client, db):
    db.rooms.insert_one({'users': [], 'testing': True})   # set up the room document for testing
    test_room = db.rooms.find_one({'testing': True})
    test_room_id = str(test_room['_id'])

    socket_client.emit('join', {'room': test_room_id, 'username': 'user_1'})

    test_room = db.rooms.find_one({'testing': True})
    assert test_room['users'] == ['user_1']

    socket_client.emit('join', {'room': test_room_id, 'username': 'user_2'})
    socket_client.emit('join', {'room': test_room_id, 'username': 'user_3'})
    socket_client.emit('join', {'room': test_room_id, 'username': 'user_4'})
    test_room = db.rooms.find_one({'testing': True})
    assert set(test_room['users']) == {'user_1', 'user_2', 'user_3', 'user_4'}


def test_is_room_full(db):
    assert False


def test_create_game_write_to_database(db):
    assert False


def test_create_game_when_room_is_not_full(db):
    assert False


def test_create_game_when_room_is_full(db):
    assert False
