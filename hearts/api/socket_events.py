from flask import session
import flask_socketio as io

from hearts import socketio


def chat(message, room):
    io.emit('chat', message, room=room)


@socketio.on('chat')
def on_chat(message):
    print('received message: ' + str(message))
    if 'room' in session:
        chat(message, session['room'])
    else:
        # chat to a global chat room?
        print('No room stored on session')


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    print('join {}'.format((username, room)))
    io.join_room(room)
    session['room'] = room
    io.emit(username + ' has entered the room.', room=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    print('leave {}'.format((username, room)))
    io.leave_room(room)
    io.emit(username + ' has left the room.', room=room)
