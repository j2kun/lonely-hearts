from flask import session
from flask import jsonify
import flask_socketio as io

from hearts import socketio
from hearts import mongo
from hearts.api.rooms import get_room
from hearts.game.hearts import Game

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


def is_room_full(room_id):
    try:
        room = get_room(room_id)
        return len(room['users']) == 4
    except:
        pass


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


def create_game(room_id):
    '''
    Returns a string game_id.
    If the room is not full, create_game will:
        -Create a Game collection document in the db
        -Store a game_id in the room
        -Create and serialize a Game object from hearts.game.hearts.py
         into the Game document.
    '''
    if is_room_full(room_id) is False:
        room = get_room(room_id)
        players = room['users']

        new_game = Game(players, points_to_win=100)
        game_data = new_game.serialize()

        game_id = mongo.db.games.insert({
            'room_id': str(room_id),
            'users': players,
            'data': game_data
        })
        mongo.db.rooms.update_one(
            {'_id': ObjectId(room_id)},
            {'$set': {'game_id': game_id}}
        )
    else:
        pass  # Room is full
