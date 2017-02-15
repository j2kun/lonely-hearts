from flask import Flask
from flask import render_template
from flask_socketio import SocketIO
from flask_socketio import emit
from pymongo import MongoClient

import settings

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY
socketio = SocketIO(app)
db_client = MongoClient(settings.DATABASE_URL)


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
    return render_template('room.html')


if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT)
