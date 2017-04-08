from flask import session
import flask_socketio as io

from hearts import socketio
from hearts import mongo


def chat(message, room):
    io.emit('chat', message, room=room)


@socketio.on('chat')
def on_chat(message):
    if 'room' in session:
        chat(message, session['room'])
    else:
        # chat to a global chat room?
        print('No room stored on session')


def is_valid_room(data):
    # Check if database document exists and contains at most 3 players.
    room = mongo.db.rooms.find_one({'room_id': data['room']})
    return (room is not None and len(room['users']) < 4)


@socketio.on('join')
def on_join(data):
    if is_valid_room(data):
        username = data['username']
        room_id = data['room']

        io.join_room(room_id)
        session['room'] = room_id
        chat(username + ' has entered the room.', room=room_id)

        mongo.db.rooms.update_one({'room_id': room_id}, {'$push': {'users': username}})
    else:
        io.disconnect()


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    io.leave_room(room)
    chat(username + ' has left the room.', room=room)
