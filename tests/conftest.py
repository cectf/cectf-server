
import pytest
from topkek import create_app
from topkek import database


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://localhost/test',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    with app.app_context():
        database.init_app(app)
        database.reset_db()
        database.init_test_db()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
