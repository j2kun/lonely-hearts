from pymongo import MongoClient
import pytest
import socketio

import settings


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
    test_db_name = 'test'
    db_client = MongoClient(settings.DATABASE_URL)
    return db_client[test_db_name]
