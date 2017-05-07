from flask import session
from flask import request
import flask_socketio as io

from hearts import socketio
from hearts import mongo
from hearts.api.rooms import get_room
from hearts.api.games import create_game
from hearts.game.hearts import Player

from bson.objectid import ObjectId


def chat(message, room):
    io.emit('chat', message, room=room)


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

        for user_info in room['users']:
            serialized_for_player = game.serialize(for_player=Player(user_info['username']))
            io.emit('game_update', serialized_for_player, room=user_info['socket_id'])


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    io.leave_room(room)
    chat(username + ' has left the room.', room=room)
