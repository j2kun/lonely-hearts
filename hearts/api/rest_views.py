import logging

from flask import current_app
from flask import jsonify
from flask import render_template
from flask import request

from hearts.api import api_blueprint as app
from hearts.api.rooms import RoomCreateFailed
from hearts.api.rooms import RoomDoesNotExist
from hearts.api.rooms import create_room
from hearts.api.rooms import get_room


logger = logging.getLogger('hearts')


@app.route('/')
def index():
    logger.info('index - viewing index.html')
    return render_template('index.html')


@app.route('/rooms/', methods=['POST'])
def rooms():
    '''
    POST /rooms/  - create a new room

    Returns:
        {
          'url': str
        }

    Visit the given url to join the created room.
    '''
    if request.method == 'POST':
        try:
            room, room_id = create_room()
            logger.info('rooms - created new room id={}'.format(room_id))
            return jsonify({
                'url': '/rooms/%s/' % room_id,
            })
        except RoomCreateFailed:
            logger.critical('rooms - failed to create a new room')


@app.route('/rooms/<room_id>/', methods=['GET'])
def room(room_id):
    '''
    GET /rooms/<room_id>/  - join a given room
    '''
    if request.method == 'GET':
        try:
            get_room(room_id)
        except RoomDoesNotExist:
            logger.info('room - attempt to join nonexistent room id={}'.format(room_id))
            render_template('index.html')

        return render_template('room.html', room_id=room_id, api_url=current_app.config['API_URL'])
