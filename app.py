from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from pymongo import MongoClient
import flask_socketio as io

import settings

app = Flask(__name__)
settings.configure(app)
socketio = io.SocketIO(app)
db_client = MongoClient(app.config['DATABASE_URL'])[app.config['DATABASE_NAME']]


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
