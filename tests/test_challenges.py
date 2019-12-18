from cectf_server import challenges
from utils import using_role

from data import challenges as data_challenges


def _get_headers(client):
    return {}  # {'Authorization': 'JWT ' + _get_token(client)}


@using_role(role='contestant')
def test_get_challenges(app, client):
    response = client.get('/api/ctf/challenges')
    assert response.status_code == 200
    assert response.json == [
        {
            'id': data_challenges[0]['id'],
            'title': data_challenges[0]['title'],
            'category': data_challenges[0]['category'],
            'author': data_challenges[0]['author'],
            'body': data_challenges[0]['body'],
            'solved': False
        },
        {
            'id': data_challenges[1]['id'],
            'title': data_challenges[1]['title'],
            'category': data_challenges[1]['category'],
            'author': data_challenges[1]['author'],
            'body': data_challenges[1]['body'],
            'solved': False
        },
    ]


@using_role(role='contestant')
def test_get_challenge(app, client):
    response = client.get('/api/ctf/challenges/' +
                          str(data_challenges[0]['id']))
    assert response.status_code == 200
    assert response.json == {
        'id': data_challenges[0]['id'],
        'title': data_challenges[0]['title'],
        'category': data_challenges[0]['category'],
        'author': data_challenges[0]['author'],
        'body': data_challenges[0]['body'],
        'solved': False
    }


@using_role(role='contestant')
def test_submit_correct_flag(app, client):
    response = client.post('/api/ctf/challenges/' + str(data_challenges[0]['id']),
                           json={'flag': 'CTF{l0l}'})
    assert response.status_code == 200
    assert response.json == {
        'status': challenges.CORRECT,
        'challenge': {
            'id': data_challenges[0]['id'],
            'title': data_challenges[0]['title'],
            'category': data_challenges[0]['category'],
            'author': data_challenges[0]['author'],
            'body': data_challenges[0]['body'],
            'solved': True
        }
    }


@using_role(role='contestant')
def test_submit_incorrect_flag(app, client):
    response = client.post('/api/ctf/challenges/' + str(data_challenges[0]['id']),
                           json={'flag': data_challenges[2]['solution']})
    assert response.status_code == 200
    assert response.json == {'status': challenges.INCORRECT}


@using_role(role='contestant')
def test_submit_twice(app, client):
    client.post('/api/ctf/challenges/' + str(data_challenges[0]['id']),
                json={'flag': data_challenges[0]['solution']})
    response = client.post('/api/ctf/challenges/' + str(data_challenges[0]['id']),
                           json={'flag': data_challenges[0]['solution']})
    assert response.status_code == 200
    assert response.json == {'status': challenges.ALREADY_SOLVED}
