from data import contestant, new_user


def test_login_no_payload(app, client):
    response = client.post('/api/auth/login')
    assert response.status_code == 400
    assert response.json == {'error': 'Request JSON is required'}


def test_login_username_not_provided(app, client):
    response = client.post('/api/auth/login', json={})
    assert response.status_code == 400
    assert response.json == {'error': 'Username is required'}


def test_login_password_not_provided(app, client):
    response = client.post('/api/auth/login', json={
        'username': contestant['username']
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Password is required'}


def test_login_username_not_found(app, client):
    response = client.post('/api/auth/login', json={
        'username': new_user['username'],
        'password': new_user['password']
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Username/password not found'}


def test_login_email_not_found(app, client):
    response = client.post('/api/auth/login', json={
        'username': new_user['email'],
        'password': new_user['password']
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Username/password not found'}


def test_login_with_username(app, client):
    response = client.post('/api/auth/login', json={
        'username': contestant['username'],
        'password': contestant['password']
    })
    assert response.status_code == 200
    assert 'authentication_token' in response.json


def test_login_with_email(app, client):
    response = client.post('/api/auth/login', json={
        'username': contestant['email'],
        'password': contestant['password']
    })
    assert response.status_code == 200
    assert 'authentication_token' in response.json


def test_login_with_username_wrong_password(app, client):
    response = client.post('/api/auth/login', json={
        'username': contestant['username'],
        'password': new_user['password']
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Username/password not found'}


def test_login_with_email_wrong_password(app, client):
    response = client.post('/api/auth/login', json={
        'username': contestant['email'],
        'password': new_user['password']
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Username/password not found'}
