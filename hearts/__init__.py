from flask import Flask
from flask_socketio import SocketIO
from flask_pymongo import PyMongo

from hearts import settings

socketio = SocketIO()
mongo = PyMongo()


def create_app():
    app = Flask(__name__)
    settings.configure(app)

    from .api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='')

    mongo.init_app(app)
    socketio.init_app(app)

    return app
