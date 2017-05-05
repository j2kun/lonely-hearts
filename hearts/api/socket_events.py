from flask import session
import flask_socketio as io

from hearts import socketio
from hearts import mongo
from hearts.api.rooms import get_room
from hearts.api.games import create_game
from hearts.api.games import GameCreateFailed

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

    io.join_room(room_id)
    session['room'] = room_id
    chat(username + ' has entered the room.', room=room_id)

    mongo.db.rooms.update_one(
        {'_id': ObjectId(room_id)},
        {'$push': {'users': username}}
        )

    room = get_room(room_id)
    if len(room['users']) == 4:
        try:
            game, game_id = create_game(room_id)

            # Emit the serialized the game view for each player here.

        except(GameCreateFailed):
            pass


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    io.leave_room(room)
    chat(username + ' has left the room.', room=room)
