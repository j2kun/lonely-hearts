import pytest
import ipdb
from bson import ObjectId

from hearts.game.hearts import Game
from hearts.api.rooms import create_room
from hearts.api.rooms import get_room
from hearts.api.games import create_game
from hearts.api.games import get_game
from hearts.api.games import save_game
from hearts.api.games import NotEnoughPlayers
from hearts.api.tests.setup import setup_room_and_game


users = [
    {'username': 'Daniel', 'socket_id': 'wat1'},
    {'username': 'Lauren', 'socket_id': 'wat2'},
    {'username': 'Erin', 'socket_id': 'wat3'},
    {'username': 'Jeremy', 'socket_id': 'wat4'},
]


def test_create_room(db):
    test_room, _ = create_room()
    assert test_room['users'] == []
    test_room2, _ = create_room(users)
    assert test_room2['users'] == users


def test_on_join_valid_room(api_client, socket_client, db):
    test_room, test_room_id = create_room()

    socket_client.emit('join', {'room': test_room_id, 'username': 'user_1'})

    test_room = get_room(test_room_id)
    assert len(test_room['users']) == 1
    for data in test_room['users']:
        assert 'username' in data
        assert 'socket_id' in data

    socket_client.emit('join', {'room': test_room_id, 'username': 'user_2'})
    socket_client.emit('join', {'room': test_room_id, 'username': 'user_3'})
    test_room = get_room(test_room_id)
    assert len(test_room['users']) == 3
    for data in test_room['users']:
        assert 'username' in data
        assert 'socket_id' in data


def test_on_join_room_is_full(db, socket_client):
    room, room_id = create_room(users)
    socket_client.emit('join', {'room': room_id, 'username': 'user_5'})
    received = socket_client.get_received()
    messages = [event for event in received if event['name'] == 'message']
    assert len(messages) == 1
    assert messages[0]['args'] == 'This room is full!'
    for user in get_room(room_id)['users']:
        assert user['username'] != 'user_5'


def test_get_game(db):
    test_room, test_room_id = create_room(users)
    game, game_id = create_game(test_room_id, deserialize=True)
    assert isinstance(game, Game)
    assert game == get_game(game_id, deserialize=True)

    serialized = get_game(game_id, deserialize=False)
    assert 'users' in serialized
    assert 'data' in serialized


def test_save_game(db):
    room, room_id = create_room(users)
    game, game_id = create_game(room_id)
    save_game(game, game_id)
    assert game.round_number == 0
    assert game == get_game(game_id)

    game.round_number += 1
    assert game.round_number == 1
    save_game(game, game_id)
    assert game == get_game(game_id)


def test_create_game_for_serialized_data(db):
    test_room, test_room_id = create_room(users)
    game, game_id = create_game(test_room_id, deserialize=False)

    expected_data = {
        'max_points': 100,
        'round_number': 0,
        'scores': [{'Lauren': 0, 'Erin': 0, 'Jeremy': 0, 'Daniel': 0}],
        'total_scores': {'Lauren': 0, 'Erin': 0, 'Jeremy': 0, 'Daniel': 0},
        'is_over': False
    }
    assert game['room_id'] == ObjectId(test_room_id)
    assert game['users'] == users
    for key in expected_data:
        assert game['data'][key] == expected_data[key]
    assert set(game['data']['players']) == set(('Lauren', 'Erin', 'Jeremy', 'Daniel'))
    assert len(game['data']['rounds']) == 1
    assert get_room(test_room_id)['game_id'] == game_id


def test_create_game_not_enough_players(db):
    test_room, test_room_id = create_room(users[:-1])
    with pytest.raises(NotEnoughPlayers):
        create_game(test_room_id)


def test_create_game_when_last_player_joins(socket_clients, db):
    room, room_id = create_room()

    usernames = ['user1', 'user2', 'user3', 'user4']
    clients = [socket_clients.new_client() for _ in range(4)]

    for username, client in zip(usernames, clients):
        client.emit('join', {'room': room_id, 'username': username})
        if username == usernames[-1]:   # When last player has joined
            assert db.games.count() == 1
        else:
            assert db.games.count() == 0

    for username, client in zip(usernames, clients):
        received_events = client.get_received()
        game_updates = [x for x in received_events if x['name'] == 'game_update']
        assert len(game_updates) == 1

        game_data = game_updates[0]['args'][0]
        rounds = game_data['rounds']
        assert len(rounds) == 1

        hands = rounds[0]['hands']
        assert username in hands
        for u in [v for v in usernames if v != username]:
            assert u not in hands


def test_pass_cards_add_to_pass_selections(db, socket_clients):
    test_env = setup_room_and_game(db, socket_clients)
    game = test_env['game']
    game_id = test_env['game_id']
    clients = test_env['clients']

    current_round = game['data']['rounds'][-1]
    hand = current_round['hands']['user4']
    cards = hand[:3]

    clients[3].emit('pass_cards', {'cards': cards})
    game = get_game(game_id, deserialize=False)
    assert len(game['data']['rounds'][-1]['pass_selections']) == 1
    assert game['data']['rounds'][-1]['pass_selections']['user4'] == cards


def test_pass_cards_add_to_pass_selections_confirmation(db, socket_clients):
    test_env = setup_room_and_game(db, socket_clients)
    game = test_env['game']
    game_id = test_env['game_id']
    clients = test_env['clients']

    current_round = game['data']['rounds'][-1]

    # user1 and user2 choose to pass their first 3 cards
    user1_cards = current_round['hands']['user1'][:3]
    user2_cards = current_round['hands']['user2'][:3]
    clients[0].emit('pass_cards', {'cards': user1_cards})
    clients[1].emit('pass_cards', {'cards': user2_cards})
    log = clients[1].get_received()
    assert log[-1]['name'] == 'pass_submission_status'
    assert log[-1]['args'][0]['status'] == 'success'
    assert 'You chose to pass' in log[-1]['args'][0]['message']

    game = get_game(game_id, deserialize=False)
    assert len(game['data']['rounds'][-1]['pass_selections']) == 2
    assert game['data']['rounds'][-1]['pass_selections']['user1'] == user1_cards
    assert game['data']['rounds'][-1]['pass_selections']['user2'] == user2_cards


def test_pass_cards_invalid_pass(db, socket_clients):
    test_env = setup_room_and_game(db, socket_clients)
    game = test_env['game']
    clients = test_env['clients']

    current_round = game['data']['rounds'][-1]

    user1_cards = current_round['hands']['user1'][:2]   # Only 2 cards chosen
    clients[0].emit('pass_cards', {'cards': user1_cards})
    log = clients[0].get_received()
    assert log[-1]['name'] == 'pass_submission_status'
    assert log[-1]['args'][0]['status'] == 'failure'
    assert 'You cannot pass' in log[-1]['args'][0]['message']


def test_pass_cards_all_users(db, socket_clients):
    '''After the server receives a 'pass_cards' event from all 4 users,
    the server should send 'pass_submission_status', 'game_update', and 'receive_cards'
    '''
    test_env = setup_room_and_game(db, socket_clients)
    game = test_env['game']
    clients = test_env['clients']
    usernames = test_env['usernames']

    current_round = game['data']['rounds'][-1]
    user_cards = [current_round['hands'][user][:3] for user in usernames]  # 3 cards from each hand
    for client, cards in zip(clients, user_cards):
        client.emit('pass_cards', {'cards': cards})

    for client in clients:
        # ipdb.set_trace()
        received_events = client.get_received()
        assert received_events[-3]['name'] == 'pass_submission_status'
        assert received_events[-2]['name'] == 'game_update'
        assert received_events[-1]['name'] == 'receive_cards'


def test_play_card_2c(db, socket_clients):
    '''
    Test that the first player can successfully play the two of
    clubs and all players receive a game update afterwards.

    '''
    test_env = setup_room_and_game(db, socket_clients, deserialize=True)
    clients = test_env['clients']
    usernames = test_env['usernames']

    game = test_env['game']
    test_round = game.rounds[-1]
    next_player = test_round.next_player

    for client, name in zip(clients, usernames):
        if next_player.username == name:
            client.emit('play_card', {'card': '2c'})  # First player plays the two of clubs.
            log = client.get_received()  # Inspect the log of the first player.
            assert log[-1]['name'] == 'game_update'
            assert log[-2]['name'] == 'play_submission_status'
            assert log[-2]['args'][0]['status'] == 'success'

    for client in clients:
        log = client.get_received()
        if len(log) != 0:       # Inspect the logs of all other players.
            assert log[-1]['name'] == 'game_update'
