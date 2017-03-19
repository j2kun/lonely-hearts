import os

import pytest
import socketio

os.environ['DATABASE_NAME'] = 'test'


@pytest.fixture(scope="session")
def api(request):
    from app import app
    app.config['TESTING'] = True
    return app.test_client()


@pytest.fixture(scope="session")
def socket(request):
    from app import app
    return socketio.test_client(app)


@pytest.fixture(scope="module")
def db(request):
    from app import db_client
    return db_client
