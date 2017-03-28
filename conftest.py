import os

import pytest
import socketio

from hearts import create_app
from hearts import mongo

os.environ['DATABASE_URL'] = 'mongodb://127.0.0.1:27017/test'
app = create_app()


@pytest.fixture(scope="session")
def api(request):
    app.config['TESTING'] = True
    return app.test_client()


@pytest.fixture(scope="session")
def socket(request):
    return socketio.test_client(app)


@pytest.fixture(scope="module")
def db(api, request):
    with app.app_context():
        return mongo.db
