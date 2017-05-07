import pytest

from hearts.api.rooms import create_room
from hearts.api.rooms import get_room
from hearts.api.games import create_game
from hearts.api.games import NotEnoughPlayers


users = [
    {'username': 'Daniel', 'socket_id': 'wat1'},
    {'username': 'Lauren', 'socket_id': 'wat2'},
    {'username': 'Erin', 'socket_id': 'wat3'},
    {'username': 'Jeremy', 'socket_id': 'wat4'},
]


def test_db(db):
    assert db.rooms.find({}).count() == 0


def test_create_room(db):
    test_room = create_room()
    assert test_room['users'] == []
    test_room2 = create_room(users)
    assert test_room2['users'] == users


def test_on_join_valid_room(api_client, socket_client, db):
    test_room = create_room()
    test_room_id = str(test_room['_id'])

    socket_client.emit('join', {'room': test_room_id, 'username': 'user_1'})

    test_room = get_room(test_room_id)
    assert len(test_room['users']) == 1
    for data in test_room['users']:
        assert 'username' in data
        assert 'socket_id' in data

    socket_client.emit('join', {'room': test_room_id, 'username': 'user_2'})
    socket_client.emit('join', {'room': test_room_id, 'username': 'user_3'})
    socket_client.emit('join', {'room': test_room_id, 'username': 'user_4'})
    test_room = get_room(test_room_id)
    assert len(test_room['users']) == 4
    for data in test_room['users']:
        assert 'username' in data
        assert 'socket_id' in data


def test_on_join_room_is_full(socket_client, db):
    # Test for an exception thrown when trying to join a full room
    pass


def test_create_game_write_to_database(db):
    test_room = create_room(users)
    test_room_id = test_room['_id']
    game, game_id = create_game(test_room_id, deserialize=False)

    expected_data = {
        'max_points': 100,
        'round_number': 0,
        'scores': [{'Lauren': 0, 'Erin': 0, 'Jeremy': 0, 'Daniel': 0}],
        'total_scores': {'Lauren': 0, 'Erin': 0, 'Jeremy': 0, 'Daniel': 0},
        'is_over': False
    }
    assert game['room_id'] == test_room_id
    assert game['users'] == users
    for key in expected_data:
        assert game['data'][key] == expected_data[key]
    assert set(game['data']['players']) == set(('Lauren', 'Erin', 'Jeremy', 'Daniel'))
    assert len(game['data']['rounds']) == 1
    assert get_room(test_room_id)['game_id'] == game_id


def test_create_game_not_enough_players(db):
    test_room = create_room(users[:-1])
    test_room_id = test_room['_id']
    with pytest.raises(NotEnoughPlayers):
        create_game(test_room_id)


def test_create_game_when_last_player_joins(socket_client, db):
    room = create_room()
    room_id = str(room['_id'])

    socket_client.emit('join', {'room': room_id, 'username': 'user_1'})
    socket_client.emit('join', {'room': room_id, 'username': 'user_2'})
    socket_client.emit('join', {'room': room_id, 'username': 'user_3'})

    assert db.games.count() == 0
    socket_client.emit('join', {'room': room_id, 'username': 'user_4'})
    assert db.games.count() == 1
