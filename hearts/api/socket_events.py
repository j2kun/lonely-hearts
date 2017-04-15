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


# Make this function a wrapper to on_join()
def is_valid_room(data):
    # Check if database document exists and contains at most 3 players.
    room_id = data['room']
    room = mongo.db.rooms.find_one({'_id': ObjectId(room_id)})
    return (room is not None and len(room['users']) < 4)


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
    new_data = mongo.db.rooms.find_one({'_id': ObjectId(room_id)})
    return jsonify(data)     # We should be returning the JSON encoding of the contents
                             # of new_data here.  Need to JSON encode the ObjectId in its
                             # '_id' field. 


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    io.leave_room(room)
    chat(username + ' has left the room.', room=room)
