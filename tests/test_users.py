from topkek_server import users
from flask_security.core import current_user

from helpers import setup_test


@setup_test('api/user', user_id=1)
def test_user(app, client):
    response = users.get_current_user_route()
    assert response.status_code == 200
    assert response.json ==\
        {"id": 1,
         "username": "a",
         "email": "a@chiquito.com",
         "roles": [
             {"name": "contestant", "description": "CTF contestant"}
         ]
         }


@setup_test('/api/user')
def test_user_not_logged_in(app, client):
    response = users.get_current_user_route()
    assert response.status_code == 400
