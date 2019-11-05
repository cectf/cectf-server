import pytest

from cectf_server import challenges
from utils import role, using_role
from data import challenges as data_challenges


@using_role(role='admin')
def test_get_challenges(app, client):
    response = client.get('/api/admin/challenges')
    print(response)
    print(dir(response))
    assert response.status_code == 200
    assert response.json == [
        data_challenges[0],
        data_challenges[1]
    ]


@using_role(role='admin')
def test_create_challenge(app, client):
    response = client.post('/api/admin/challenges',
                           json={
                               'title': data_challenges[2]['title'],
                               'category': data_challenges[2]['category'],
                               'body': data_challenges[2]['body'],
                               'hint': data_challenges[2]['hint'],
                               'solution': data_challenges[2]['solution']
                           })
    print(response.json)
    assert response.status_code == 200
    assert response.json == data_challenges[2]


@using_role(role='admin')
def test_create_challenge_missing_title(app, client):
    with pytest.raises(KeyError):
        client.post('/api/admin/challenges',
                    json={
                        'category': data_challenges[2]['category'],
                        'body': data_challenges[2]['body'],
                        'hint': data_challenges[2]['hint'],
                        'solution': data_challenges[2]['solution']
                    })


def test_created_challenge_can_be_solved(app, client):
    with role(client, 'admin'):
        client.post('/api/admin/challenges',
                    json={
                        'title': data_challenges[2]['title'],
                        'category': data_challenges[2]['category'],
                        'body': data_challenges[2]['body'],
                        'hint': data_challenges[2]['hint'],
                        'solution': data_challenges[2]['solution']
                    })
    with role(client, 'contestant'):
        response = client.post('/api/ctf/challenges/' + str(data_challenges[2]['id']),
                               json={'flag': data_challenges[2]['solution']})
        assert response.status_code == 200
        assert response.json == {
            'status': challenges.CORRECT,
            'challenge': {
                'id': data_challenges[2]['id'],
                'title': data_challenges[2]['title'],
                'category': data_challenges[2]['category'],
                'body': data_challenges[2]['body'],
                'solution': data_challenges[2]['solution'],
                'hinted': False,
                'solved': True
            }
        }


@using_role(role='admin')
def test_update_challenge(app, client):
    response = client.post('/api/admin/challenges/' + str(data_challenges[0]['id']),
                           json={
                               'title': data_challenges[2]['title'],
                               'category': data_challenges[2]['category'],
                               'body': data_challenges[2]['body'],
                               'hint': data_challenges[2]['hint'],
                               'solution': data_challenges[2]['solution']

    })
    assert response.status_code == 200
    assert response.json == {
        'id': data_challenges[0]['id'],
        'title': data_challenges[2]['title'],
        'category': data_challenges[2]['category'],
        'body': data_challenges[2]['body'],
        'hint': data_challenges[2]['hint'],
        'solution': data_challenges[2]['solution']
    }


@using_role(role='admin')
def test_update_challenge_no_change(app, client):
    response = client.post('/api/admin/challenges/' + str(data_challenges[0]['id']),
                           json={})
    assert response.status_code == 200
    assert response.json == data_challenges[0]


@using_role(role='admin')
def test_delete_challenge(app, client):
    response = client.delete('/api/admin/challenges/' +
                             str(data_challenges[0]['id']))
    assert response.status_code == 200
