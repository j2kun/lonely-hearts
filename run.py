from hearts import create_app
from hearts import socketio

import os
import sys
import logging
from flask import Flask

app = create_app()

if 'DYNO' in os.environ:
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.INFO)

if app.config['DEBUG']:
    socketio.run(
        app,
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
