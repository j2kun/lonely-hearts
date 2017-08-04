'''
Documentation for the various socket events sent from the 
server to the client:

    'chat':   A message to all players in a room.
    'message':   An error message sent to a player.
    'game_update':   A private serialized view of a game object.
    'pass_submission_status':
        Server determines if the 'pass_cards' event data is valid.
        {
         'status': 'success'|'failure'
         'message': error string
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
from hearts.api.strings import ROOM_IS_FULL
from hearts.game.hearts import Card

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


def create_player(room, socket_id):
    '''
    Create a Player object based on the socket_id of the user in the room.
    '''
    username = None
    for user_data in room['users']:
        if user_data['socket_id'] == socket_id:
            username = user_data['username']
            return Player(username)


def emit_game_updates(room, game):
    '''
    Emit a serialized view of the game to each player in the room.
    '''
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
    '''
    socket_id = request.sid
    game_id = game_id_lookup()
    game = get_game(game_id)
    current_round = game.rounds[-1]
    cards = [Card.deserialize(a) for a in data['cards']]
    room = get_room(session['room'])

    player = create_player(room, socket_id)
    confirmation = {'status': 'success'}
    try:
        current_round.add_to_pass_selections(player, cards)
        save_game(game, game_id)
    except ValueError as error_message:
        confirmation['status'] = 'failure'
        confirmation['message'] = str(error_message)
    finally:
        io.emit('pass_submission_status', confirmation, room=socket_id)
        if len(current_round.pass_selections) == 4:
            current_round.pass_cards()
            save_game(game, game_id)
            emit_game_updates(room, game)
