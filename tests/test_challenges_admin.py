import pytest

from cectf_server import challenges
from helpers import role, using_role


@using_role(role='admin')
def test_get_challenges(app, client):
    response = client.get('/api/admin/challenges')
    assert response.status_code == 200
    assert response.json == [
        {
            'id': 1,
            'title': 'The First Challenge',
            'category': 'crypto',
            'body': 'Just think really hard!',
            'hint': 'CTF{l0l}',
            'solution': 'CTF{l0l}'
        },
        {
            'id': 2,
            'title': 'The Second Challenge',
            'category': 'reversing',
            'body': 'Just think really harder!',
            'hint': 'no cheatin',
            'solution': 'CTF{1337}'
        }
    ]


@using_role(role='admin')
def test_create_challenge(app, client):
    response = client.post('/api/admin/challenges',
                           json={
                               'title': 'The Third Challenge',
                               'category': 'web',
                               'body': 'testing 123',
                               'hint': 'hint123',
                               'solution': 'CTF{123}'
                           })
    assert response.status_code == 200
    assert response.json == {
        'id': 3,
        'title': 'The Third Challenge',
        'category': 'web',
        'body': 'testing 123',
        'hint': 'hint123',
        'solution': 'CTF{123}'
    }


@using_role(role='admin')
def test_create_challenge_missing_title(app, client):
    with pytest.raises(KeyError):
        response = client.post('/api/admin/challenges', json={
            'category': 'web',
            'body': 'testing 123',
            'hint': 'hint123',
            'solution': 'CTF{123}'
        })


def test_created_challenge_can_be_solved(app, client):
    with role(client, 'admin'):
        client.post('/api/admin/challenges', json={
            'title': 'The Third Challenge',
            'category': 'web',
            'body': 'testing 123',
            'hint': 'hint123',
            'solution': 'CTF{123}'
        })
    with role(client, 'contestant'):
        response = client.post('/api/ctf/challenges/3',
                               json={'flag': 'CTF{123}'})
        assert response.status_code == 200
        assert response.json == {
            'status': challenges.CORRECT,
            'challenge': {
                'id': 3,
                'title': 'The Third Challenge',
                'category': 'web',
                'body': 'testing 123',
                'hinted': False,
                'solved': True,
                'solution': 'CTF{123}'
            }
        }


@using_role(role='admin')
def test_update_challenge(app, client):
    response = client.post('/api/admin/challenges/1', json={
        'title': 'The New First Challenge',
        'category': 'cryptozoology',
        'body': 'BIGGER AND BADDER',
        'hint': 'HINTS ARE FER NERDS',
        'solution': 'CTF{S0_MUCH_M0R3_C0MPLIC4T3D}'
    })
    assert response.status_code == 200
    assert response.json == {
        'id': 1,
        'title': 'The New First Challenge',
        'category': 'cryptozoology',
        'body': 'BIGGER AND BADDER',
        'hint': 'HINTS ARE FER NERDS',
        'solution': 'CTF{S0_MUCH_M0R3_C0MPLIC4T3D}'
    }


@using_role(role='admin')
def test_update_challenge_no_change(app, client):
    response = client.post('/api/admin/challenges/1', json={})
    assert response.status_code == 200
    assert response.json == {
        'id': 1,
        'title': 'The First Challenge',
        'category': 'crypto',
        'body': 'Just think really hard!',
        'hint': 'CTF{l0l}',
        'solution': 'CTF{l0l}'
    }


@using_role(role='admin')
def test_delete_challenge(app, client):
    response = client.delete('/api/admin/challenges/1')
    assert response.status_code == 200
