from flask import session
from flask import jsonify
import flask_socketio as io

from hearts import socketio
from hearts import mongo

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

    # refactor this as a separate function
    mongo.db.rooms.update_one(
        {'_id': ObjectId(room_id)},
        {'$push': {'users': username}}
        )

    new_data = mongo.db.rooms.find_one(
        {'_id': ObjectId(room_id)},
        projection={'_id': False}
        )
    return jsonify(new_data)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    io.leave_room(room)
    chat(username + ' has left the room.', room=room)
