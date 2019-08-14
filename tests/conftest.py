
import pytest
from topkek import create_app
from topkek import db


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DATABASE': 'test'
    })

    with app.app_context():
        db.init_db()
        db.init_test_db()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
