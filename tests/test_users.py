from utils import using_role
from cectf_server.test_data import contestant


@using_role(role='contestant')
def test_user(app, client):
    response = client.get('/api/user')
    assert response.status_code == 200
    assert response.json == {
        'id': contestant['id'],
        'username': contestant['username'],
        'email': contestant['email'],
        'roles': [
            {'name': 'contestant', 'description': 'CTF contestant'}
        ]
    }


def test_user_not_logged_in(app, client):
    response = client.get('/api/user')
    assert response.status_code == 400
