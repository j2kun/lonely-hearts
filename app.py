from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import session
from flask_socketio import SocketIO
from flask_socketio import emit
from flask_socketio import join_room
from flask_socketio import leave_room
from pymongo import MongoClient

import settings

app = Flask(__name__)
settings.configure(app)
socketio = SocketIO(app)
db_client = MongoClient(app.config['DATABASE_URL'])[app.config['DATABASE_NAME']]


def chat(message, room):
    emit('chat', message, room=room)


@socketio.on('chat')
def on_chat(message):
    print('received message: ' + str(message))
    if 'room' in session:
        chat(message, session['room'])
    else:
        print('No room stored on session')


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    print('join {}'.format((username, room)))
    join_room(room)
    session['room'] = room
    emit(username + ' has entered the room.', room=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    print('leave {}'.format((username, room)))
    leave_room(room)
    emit(username + ' has left the room.', room=room)


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
    # reminder: don't use this in production, instead use WSGI
    app.run(host=app.config['HOST'])
