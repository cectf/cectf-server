from topkek import users


def test_users_id(client):
    response = client.get('/api/app/users/1')
    assert response.data == b'{"admin":false,"id":1,"password":"b","username":"a"}\n'


def test_users_id_missing(client):
    response = client.get('/api/app/users/id/0')
    assert response.status_code == 404


def test_users_username(client):
    response = client.get('/api/app/users/username/a')
    assert response.data == b'{"admin":false,"id":1,"password":"b","username":"a"}\n'


def test_users_username_missing(client):
    response = client.get('/api/app/users/username/aaaa')
    assert response.status_code == 404
