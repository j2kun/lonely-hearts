from flask import jsonify
from flask import render_template
from flask import request

from hearts.api import api_blueprint as app
from hearts import mongo

from bson.objectid import ObjectId


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rooms/', methods=['POST'])
def rooms():
    if request.method == 'POST':
        # Room ids are the unique database document ids
        room_id = mongo.db.rooms.insert({'users': []})
        if room_id:
            room = mongo.db.rooms.find_one({'_id': room_id})
            room['room_id'] = str(room_id)
            return jsonify({
                'url': '/rooms/%s/' % room_id,
                'id': str(room_id),
            })


@app.route('/rooms/<room_id>/', methods=['GET'])
def room(room_id):
    if request.method == 'GET':
        result = mongo.db.rooms.find_one({'_id': ObjectId(room_id)})
        if not result:
            render_template('index.html')
        return render_template('room.html', room_id=room_id)
