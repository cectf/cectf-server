
import pytest
from topkek_server import create_app
from topkek_server import database
from topkek_server.models import User


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://travis@localhost/test',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test',
        'SECURITY_PASSWORD_SALT': 'test',
    })

    with app.app_context():
        database.init_app(app)
        database.reset_db()
        database.init_test_db()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
