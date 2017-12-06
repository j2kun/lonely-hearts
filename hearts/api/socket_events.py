'''
Documentation for the various socket events sent from the
server to the client:

    'chat':   A message to all players in a room.

    'message':   An error message sent to a player.

    'game_update':   A private serialized view of a game object.

    'pass_submission_status':
        Server determines if the 'pass_cards' event data is valid.
        {
         'status': 'success'|'failure',
         'message': error string
        }

    'receive_cards':    A list and description of the cards a user receives.
        {
         'cards': [str, str, str],
         'message': str
        }

    'play_submission_status':
        {
         'status': 'success'|'failure',
         'message': str
        }
'''

from flask import session
from flask import request
import flask_socketio as io

from hearts import socketio
from hearts import mongo
from hearts.api.rooms import get_room
from hearts.api.games import create_game
from hearts.api.games import get_game
from hearts.api.games import save_game
from hearts.game.hearts import Player
from hearts.game.hearts import Card
from hearts.api.strings import ROOM_IS_FULL
from hearts.api.strings import played_a_card
from hearts.api.strings import pass_submit
from hearts.api.strings import received_cards_from

from bson.objectid import ObjectId


def chat(message, room):
    io.emit('chat', message, room=room)


def game_id_lookup():
    '''
    Returns the game_id of the client making a socket request
    through the session variable.  If not present, looks up the
    game_id from the room object in the database and saves it in
    the session.
    '''
    if 'game' in session:
        return session['game']
    else:
        room = get_room(session['room'])
        if 'game_id' in room:
            session['game'] = room['game_id']
            return session['game']
        else:
            raise Exception('User is currently not in a game!')


def player_from_sid(room, socket_id):
    '''
    Create a Player object based on the socket_id of the user in the room.
    '''
    username = None
    for user_data in room['users']:
        if user_data['socket_id'] == socket_id:
            username = user_data['username']
            return Player(username)


def sid_from_player(room, player):
    '''Retrieve the socket id of a Player object or username
    in the room.
    '''
    for user_data in room['users']:
        if user_data['username'] == player:
            return user_data['socket_id']


def emit_game_updates(room, game, player_id=None):
    '''
    Emit a serialized view of the game to each player in the room.
    Using the optional player_id argument will update only for that player.
    '''
    if player_id:
            for_player = player_from_sid(room, player_id)
            serialized_for_player = game.serialize(for_player=for_player)
            io.emit('game_update', serialized_for_player, room=player_id)
    else:
        for user_info in room['users']:
            serialized_for_player = game.serialize(for_player=Player(user_info['username']))
            io.emit('game_update', serialized_for_player, room=user_info['socket_id'])


@socketio.on('chat')
def on_chat(message):
    if 'room' in session:
        chat(message, session['room'])
    else:
        # chat to a global chat room?
        print('No room stored on session')


@socketio.on('join')
def on_join(data):
    username = data['username']
    room_id = data['room']

    '''
    The request context global is enhanced with a sid member that is set to a
    unique session ID for the connection. This value is used as an initial room
    where the client is added.
    '''
    socket_id = request.sid

    if len(get_room(room_id)['users']) >= 4:
        io.emit('message', ROOM_IS_FULL, room=socket_id)

    else:
        io.join_room(room_id)
        session['room'] = room_id
        mongo.db.rooms.update_one(
            {'_id': ObjectId(room_id)},
            {'$push': {'users': {'username': username, 'socket_id': socket_id}}}
        )
        chat(username + ' has entered the room.', room=room_id)

        room = get_room(room_id)
        if len(room['users']) == 4:
            game, game_id = create_game(room_id, max_points=100)
            session['game'] = str(game_id)

            chat('The Hearts game has started.', room=room_id)
            emit_game_updates(room, game)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    io.leave_room(room)
    chat(username + ' has left the room.', room=room)


@socketio.on('pass_cards')
def on_pass_cards(data):
    '''
    data: {'cards': [str, str, str]}
    Returns:
        {
            'status': 'success'||'failure',
            'message': str
        }
    '''
    socket_id = request.sid
    room = get_room(session['room'])

    game_id = game_id_lookup()
    game = get_game(game_id)
    current_round = game.rounds[-1]

    player = player_from_sid(room, socket_id)
    cards = [Card.deserialize(a) for a in data['cards']]
    confirmation = {
        'status': 'success',
        'message': pass_submit(data['cards'])
    }
    try:
        current_round.add_to_pass_selections(player, cards)
        emit_game_updates(room, game, player_id=socket_id)
        save_game(game, game_id)
    except ValueError as error_message:
        confirmation['status'] = 'failure'
        confirmation['message'] = str(error_message)

    io.emit('pass_submission_status', confirmation, room=socket_id)   # Remove this. Return the confirmation
                                                                      # instead of emitting it.

    if len(current_round.pass_selections) == 4:
        received_cards = current_round.pass_cards()
        current_round.set_playing_states()

        # Remove this.  Passing messages are updated via current_round.update_messages_after_passing()
        '''Notify each player of the cards they received.'''
        for user_data in room['users']:
            receiver_id = user_data['socket_id']
            receiver = Player(user_data['username'])
            cards = received_cards[receiver]['cards']
            passer = received_cards[receiver]['from']

            data = {
                'cards': cards,
                'message': received_cards_from(passer, cards)
            }
            io.emit('receive_cards', data, room=receiver_id)

        current_round.update_messages_after_passing(received_cards)
        save_game(game, game_id)
        emit_game_updates(room, game)
    return confirmation


@socketio.on('play_card')
def on_play_card(data):
    socket_id = request.sid
    room = get_room(session['room'])

    game_id = game_id_lookup()
    game = get_game(game_id)
    current_round = game.rounds[-1]

    player = player_from_sid(room, socket_id)
    card = Card.deserialize(data['card'])

    confirmation = {
        'status': 'success',
        'message': played_a_card(player, card)
    }
    try:
        current_round.play_card(player, card)
        save_game(game, game_id)
    except ValueError as error_message:
        confirmation['status'] = 'failure'
        confirmation['message'] = str(error_message)

    io.emit('play_submission_status', confirmation, room=socket_id)

    if confirmation['status'] == 'success':
        # check if game is over to notify score update
        if current_round.is_over():
            data = {'message': 'The round is over! The scores have been updated'}
            io.emit('round_over', data, room=socket_id)
        if game.is_over():
            data = {'message': 'The game is over! The final scores have been updated'}
            io.emit('game_over', data, room=socket_id)
        emit_game_updates(room, game)
        save_game(game, game_id)
