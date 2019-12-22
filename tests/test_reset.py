
from cectf_server import create_app


def test_reset_testing():
    app = create_app({
        'TESTING': False,
        'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://travis@localhost/test',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test',
        'SECURITY_PASSWORD_SALT': 'test',
        'CECTF_FILE_LOCATION': '/tmp/ctf/test',
        'CECTF_PRODUCTION': False
    })
    client = app.test_client()
    response = client.get('/api/test/reset')
    assert response.status_code == 204


def test_reset_production():
    app = create_app({
        'TESTING': False,
        'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://travis@localhost/test',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test',
        'SECURITY_PASSWORD_SALT': 'test',
        'CECTF_FILE_LOCATION': '/tmp/ctf/test',
        'CECTF_PRODUCTION': True
    })
    client = app.test_client()
    response = client.get('/api/test/reset')
    assert response.status_code == 400
