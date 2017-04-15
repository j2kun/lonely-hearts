import os

import pytest

from hearts import create_app
from hearts import mongo
from hearts import socketio

database_name = 'test'
os.environ['DATABASE_URL'] = 'mongodb://127.0.0.1:27017/{}'.format(database_name)
app = create_app()


@pytest.fixture(scope="session")
def api_client(request):
    app.config['TESTING'] = True
    return app.test_client()


@pytest.fixture(scope="session")
def socket_client(request):
    client = socketio.test_client(app)
    client.get_received()  # clears the 'connected' event
    return client


@pytest.fixture
def db(api_client, request):
    with app.app_context():
        mongo.db.command('dropDatabase')
        return mongo.db
