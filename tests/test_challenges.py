from topkek import challenges


def _get_token(client):
    response = client.post(
        '/api/login/auth', json={'username': 'a', 'password': 'b'})
    return response.json['access_token']


def _get_headers(client):
    return {}  # {'Authorization': 'JWT ' + _get_token(client)}


def test_get_challenges(app, client):
    response = client.get('/api/app/users/1/challenges',
                          headers=_get_headers(client))
    assert response.status_code == 200
    assert len(response.json) == 2
    challenge1 = response.json[0]
    assert challenge1['id'] == 1
    assert challenge1['title'] == 'The First Challenge'
    assert challenge1['solved'] == False
    assert challenge1['hinted'] == False
    challenge2 = response.json[1]
    assert challenge2['id'] == 2
    assert challenge2['title'] == 'The Second Challenge'
    assert challenge2['solved'] == False
    assert challenge2['hinted'] == False


def test_get_challenge(app, client):
    response = client.get('/api/app/users/1/challenges/1',
                          headers=_get_headers(client))
    assert response.status_code == 200
    print(response.json)
    assert response.json['id'] == 1
    assert response.json['title'] == 'The First Challenge'
    assert response.json['solved'] == False
    assert response.json['hinted'] == False
    assert 'solution' not in response.json
    assert 'hint' not in response.json


def test_submit_correct_flag(app, client):
    response = client.post('/api/app/users/1/challenges/1',
                           headers=_get_headers(client),
                           json={'flag': 'CTF{l0l}'})
    assert response.status_code == 200
    print(response.json)
    assert response.json == {
        'status': challenges.CORRECT,
        'challenge': {
            'id': 1,
            'title': 'The First Challenge',
            'category': 'crypto',
            'body': 'Just think really hard!',
            'solved': True,
            'solution': 'CTF{l0l}',
            'hinted': False}}


def test_submit_incorrect_flag(app, client):
    response = client.post('/api/app/users/1/challenges/1',
                           headers=_get_headers(client),
                           json={'flag': 'CTF{l0l_n0p3}'})
    assert response.status_code == 200
    print(response.json)
    assert response.json == {'status': challenges.INCORRECT}


def test_submit_twice(app, client):
    client.post('/api/app/users/1/challenges/1',
                headers=_get_headers(client),
                json={'flag': 'CTF{l0l}'})
    response = client.post('/api/app/users/1/challenges/1',
                           headers=_get_headers(client),
                           json={'flag': 'CTF{l0l}'})
    assert response.status_code == 200
    print(response.json)
    assert response.json == {'status': challenges.ALREADY_SOLVED}
