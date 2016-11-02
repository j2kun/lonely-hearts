import os
import dotenv

from flask import Flask
from flask import render_template
from flask import request
from flask.json import jsonify
from flask_socketio import SocketIO
# from flask_socketio import emit
from pymongo import MongoClient

'''
    Load the configuration variables from .env
'''
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'abc123')
socketio = SocketIO(app)
db_client = MongoClient(os.environ.get('DATABASE_URL'))


'''
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
'''


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tables/', methods=['POST'])
def tables():
    if request.method == 'POST':
        # generate a random hash
        # and make sure it's not in the db already
        return jsonify(id='blah')


if __name__ == '__main__':
    socketio.run(app)
