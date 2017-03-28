from flask import Blueprint

api_blueprint = Blueprint('api', __name__)

from hearts.api import socket_events
from hearts.api import rest_views
