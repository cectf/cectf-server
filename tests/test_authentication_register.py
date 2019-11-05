from data import contestant, new_user, challenges


def test_register_json_not_provided(app, client):
    response = client.post('/api/auth/register')
    assert response.status_code == 400
    assert response.json == {'error': 'Request JSON is required'}


def test_register_email_not_provided(app, client):
    response = client.post('/api/auth/register', json={
        'password': new_user['password'],
        'username': new_user['username']
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Email is required'}


def test_register_password_not_provided(app, client):
    response = client.post('/api/auth/register', json={
        'email': new_user['email'],
        'username': new_user['username']
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Password is required'}


def test_register_username_not_provided(app, client):
    response = client.post('/api/auth/register', json={
        'email': new_user['email'],
        'password': new_user['password']
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Username is required'}


def test_register_email_formatted_incorrectly(app, client):
    response = client.post('/api/auth/register', json={
        'email': 'email',
        'password': new_user['password'],
        'username': new_user['username']
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Email is formatted incorectly'}


def test_register_email_too_long(app, client):
    response = client.post('/api/auth/register', json={
        'email': ('x' * 3000) + '@ctf.chiquito.us',
        'password': new_user['password'],
        'username': new_user['username']
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Email is too long'}


def test_register_email_exists(app, client):
    response = client.post('/api/auth/register', json={
        'email': contestant['email'],
        'password': new_user['password'],
        'username': new_user['username']
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Email is already registered'}


def test_register_username_too_short(app, client):
    response = client.post('/api/auth/register', json={
        'email': new_user['email'],
        'password': new_user['password'],
        'username': 'x'
    })
    assert response.status_code == 400
    assert response.json == {
        'error': 'Username must have 3 or more characters'}


def test_register_username_too_long(app, client):
    response = client.post('/api/auth/register', json={
        'email': new_user['email'],
        'password': new_user['password'],
        'username': 'x' * 3000
    })
    assert response.status_code == 400
    assert response.json == {
        'error': 'Username is too long'}


def test_register_username_exists(app, client):
    response = client.post('/api/auth/register', json={
        'email': new_user['email'],
        'password': new_user['password'],
        'username': contestant['username']
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Username is already registered'}


def test_register_password_in_dictionary(app, client):
    response = client.post('/api/auth/register', json={
        'email': new_user['email'],
        'password': 'password',
        'username': new_user['username']
    })
    assert response.status_code == 400
    assert response.json == {
        'error': 'good god why would you choose that password'}


def test_register_password_too_short(app, client):
    response = client.post('/api/auth/register', json={
        'email': new_user['email'],
        'password': '',
        'username': new_user['username']
    })
    assert response.status_code == 400
    assert response.json == {
        'error': 'Password must have 6 or more characters'}


def test_register_success(app, client):
    response = client.post('/api/auth/register', json={
        'email': new_user['email'],
        'password': new_user['password'],
        'username': new_user['username']
    })
    assert response.status_code == 200
    assert 'authentication_token' in response.json

    # get challenges to verify we are logged in as a new contestant
    response = client.get('/api/ctf/challenges')
    assert response.status_code == 200
    assert response.json == [
        {
            'id': challenges[0]['id'],
            'title': challenges[0]['title'],
            'category': challenges[0]['category'],
            'body': challenges[0]['body'],
            'hinted': False,
            'solved': False
        },
        {
            'id': challenges[1]['id'],
            'title': challenges[1]['title'],
            'category': challenges[1]['category'],
            'body': challenges[1]['body'],
            'hinted': False,
            'solved': False
        },
    ]
