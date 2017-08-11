from hearts.api.rooms import create_room
from hearts.api.rooms import get_room
from hearts.api.games import get_game


def setup_room_and_game(db, socket_clients, deserialize=False):
    room, room_id = create_room()
    usernames = ['user1', 'user2', 'user3', 'user4']
    clients = [socket_clients.new_client() for _ in range(4)]

    for username, client in zip(usernames, clients):
        client.emit('join', {'room': room_id, 'username': username})  # Last user to join starts the game
    room = get_room(room_id)
    game_id = str(room['game_id'])

    return {
        'clients': clients,
        'usernames': usernames,
        'room': get_room(room_id),
        'room_id': room_id,
        'game_id': game_id,
        'game': get_game(game_id, deserialize=deserialize)
    }
