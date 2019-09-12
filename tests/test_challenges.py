from cectf_server import challenges
from helpers import using_role


def _get_headers(client):
    return {}  # {'Authorization': 'JWT ' + _get_token(client)}


@using_role(role='contestant')
def test_get_challenges(app, client):
    response = client.get('/api/ctf/challenges')
    assert response.status_code == 200
    assert response.json == [
        {
            'id': 1,
            'title': 'The First Challenge',
            'category': 'crypto',
            'body': 'Just think really hard!',
            'hinted': False,
            'solved': False
        },
        {
            'id': 2,
            'title': 'The Second Challenge',
            'category': 'reversing',
            'body': 'Just think really harder!',
            'hinted': False,
            'solved': False
        }
    ]


@using_role(role='contestant')
def test_get_challenge(app, client):
    response = client.get('/api/ctf/challenges/1')
    assert response.status_code == 200
    assert response.json == {
        'id': 1,
        'title': 'The First Challenge',
        'category': 'crypto',
        'body': 'Just think really hard!',
        'hinted': False,
        'solved': False
    }


@using_role(role='contestant')
def test_submit_correct_flag(app, client):
    response = client.post('/api/ctf/challenges/1', json={'flag': 'CTF{l0l}'})
    assert response.status_code == 200
    assert response.json == {
        'status': challenges.CORRECT,
        'challenge': {
            'id': 1,
            'title': 'The First Challenge',
            'category': 'crypto',
            'body': 'Just think really hard!',
            'hinted': False,
            'solved': True,
            'solution': 'CTF{l0l}'
        }
    }


@using_role(role='contestant')
def test_submit_incorrect_flag(app, client):
    response = client.post('/api/ctf/challenges/1',
                           json={'flag': 'CTF{l0l_n0p3}'})
    assert response.status_code == 200
    assert response.json == {'status': challenges.INCORRECT}


@using_role(role='contestant')
def test_submit_twice(app, client):
    client.post('/api/ctf/challenges/1', json={'flag': 'CTF{l0l}'})
    response = client.post('/api/ctf/challenges/1', json={'flag': 'CTF{l0l}'})
    assert response.status_code == 200
    assert response.json == {'status': challenges.ALREADY_SOLVED}
