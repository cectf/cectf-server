import shutil
import pytest
from flask import testing
from werkzeug.datastructures import Headers
from cectf_server import create_app
from cectf_server import database
from cectf_server.models import User


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://travis@localhost/test',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test',
        'SECURITY_PASSWORD_SALT': 'test',
        'CECTF_FRONTEND_DOMAIN': 'http://localhost',
        'CECTF_FILE_LOCATION': '/tmp/ctf/test',
    })

    with app.app_context():
        database.init_app(app)
        database.reset_db()
        database.init_test_db()

    try:
        shutil.rmtree(app.config['CECTF_FILE_LOCATION'])
    except OSError:
        pass

    yield app


class TestClient(testing.FlaskClient):
    def __init__(self, *args, **kwargs):
        self.csrf_token = ""
        super().__init__(*args, **kwargs)
        self.csrf_token = self.get('/api/csrf').json['csrf_token']

    def open(self, *args, **kwargs):
        api_key_headers = Headers({
            'X-CSRFToken': self.csrf_token
        })
        headers = kwargs.pop('headers', Headers())
        if type(headers) is not Headers:
            headers = Headers(headers)
        headers.extend(api_key_headers)
        kwargs['headers'] = headers
        return super().open(*args, **kwargs)


@pytest.fixture
def client(app):
    app.test_client_class = TestClient
    return app.test_client()
