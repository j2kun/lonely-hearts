import pytest

from hearts.api.rooms import create_room
from hearts.api.rooms import get_room
from hearts.api.games import create_game
from hearts.api.games import get_game
from hearts.api.games import NotEnoughPlayers


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


def test_on_join_room_is_full(socket_client, db):
    # Test for an exception thrown when trying to join a full room
    pass


def test_create_game_write_to_database(db):
    test_room = create_room(('Lauren', 'Erin', 'Jeremy', 'Daniel'))
    test_room_id = test_room['_id']

    game, game_id = create_game(test_room_id)

    expected_data = {
        'players': ['Lauren', 'Erin', 'Jeremy', 'Daniel'],
        'max_points': 100,
        'rounds': [],
        'round_number': 0,
        'scores': [],
        'total_scores': {'Lauren': 0, 'Erin': 0, 'Jeremy': 0, 'Daniel': 0},
        'is_over': False
    }
    game = get_game(game_id)
    assert game['room_id'] == test_room_id
    assert game['users'] == ['Lauren', 'Erin', 'Jeremy', 'Daniel']
    for key in expected_data:
        assert game['data'][key] == expected_data[key]

    assert get_room(test_room_id)['game_id'] == game_id


def test_create_game_not_enough_players(db):
    test_room = create_room(('Lauren', 'Erin', 'Jeremy'))
    test_room_id = test_room['_id']
    with pytest.raises(NotEnoughPlayers):
        game, game_id = create_game(test_room_id)


def test_create_game_when_last_player_joins(db):
    assert False
