from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import session
from pymongo import MongoClient
import flask_socketio as io

import settings

app = Flask(__name__)
settings.configure(app)
socketio = io.SocketIO(app)
db_client = MongoClient(app.config['DATABASE_URL'])[app.config['DATABASE_NAME']]


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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rooms/', methods=['POST'])
def rooms():
    if request.method == 'POST':
        room_id = db_client.rooms.insert({})
        if room_id:
            return jsonify({
                'url': '/rooms/%s/' % room_id,
                'id': str(room_id),
            })


@app.route('/rooms/<room_id>/', methods=['GET'])
def room(room_id):
    if request.method == 'GET':
        result = db_client.rooms.find_one({'_id': room_id})
        if not result:
            render_template('index.html')
        return render_template('room.html', room_id=room_id)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
