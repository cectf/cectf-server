from topkek import authentication


def test_login_app(client):
    response = client.post(
        '/api/login/auth', json={'username': 'a', 'password': 'b'})
    assert response.status_code == 200
    assert 'access_token' in response.json


def test_login_admin(client):
    response = client.post(
        '/api/login/auth', json={'username': 'abc', 'password': '123'})
    assert response.status_code == 200
    assert 'access_token' in response.json


def test_failed_login_app(client):
    response = client.post(
        '/api/login/auth', json={'username': 'b', 'password': 'a'})
    assert response.status_code == 401
