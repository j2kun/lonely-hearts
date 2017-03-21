from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask_socketio import SocketIO
from flask_socketio import emit
from pymongo import MongoClient

import settings

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY
socketio = SocketIO(app)
db_client = MongoClient(settings.DATABASE_URL)[settings.DATABASE_NAME]


@socketio.on('chat message', namespace='/chat')
def handle_chat_message(json):
    print('received message: ' + str(json))
    emit('chat message', str(json), broadcast=True)


@socketio.on('connect')  # global namespace
def handle_connect():
    print('Client connected')


@socketio.on('connect', namespace='/chat')
def handle_chat_connect():
    print('Client connected to chat namespace')
    emit('chat message', 'welcome!')


@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    print('Client disconnected')


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
        return render_template('room.html', room_data=room_id)


if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT)
