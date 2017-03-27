from flask import Flask
from pymongo import MongoClient
import flask_socketio as io

import settings

app = Flask(__name__)
settings.configure(app)
socketio = io.SocketIO(app)
db_client = MongoClient(app.config['DATABASE_URL'])[app.config['DATABASE_NAME']]


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
