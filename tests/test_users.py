from helpers import using_role


@using_role(role='contestant')
def test_user(app, client):
    response = client.get('/api/user')
    assert response.status_code == 200
    assert response.json == \
           {'id': 1,
            'username': 'a',
            'email': 'a@chiquito.com',
            'roles': [
                {'name': 'contestant', 'description': 'CTF contestant'}
            ]
            }


def test_user_not_logged_in(app, client):
    response = client.get('/api/user')
    assert response.status_code == 400
