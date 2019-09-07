from cectf_server import challenges_admin, challenges

from helpers import setup_test


@setup_test('/api/admin/challenges', user_id=2)
def test_get_challenges(app, client):
    response = challenges_admin.get_challenges()
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


@setup_test('/api/admin/challenges',
            method='POST',
            json={
                'title': 'The Third Challenge',
                'category': 'web',
                'body': 'testing 123',
                'hint': 'hint123',
                'solution': 'CTF{123}'
            },
            user_id=2)
def test_create_challenge(app, client):
    response = challenges_admin.create_challenge()
    assert response.status_code == 200
    assert response.json == {
        'id': 3,
        'title': 'The Third Challenge',
        'category': 'web',
        'body': 'testing 123',
        'hint': 'hint123',
        'solution': 'CTF{123}'
    }


@setup_test('/api/admin/challenges',
            method='POST',
            json={
                'category': 'web',
                'body': 'testing 123',
                'hint': 'hint123',
                'solution': 'CTF{123}'
            },
            user_id=2)
def test_create_challenge_missing_title(app, client):
    try:
        response = challenges_admin.create_challenge()
        assert 'Expected KeyError' == None
    except KeyError:
        pass


@setup_test('/api/admin/challenges',
            method='POST',
            json={
                'title': 'The Third Challenge',
                'category': 'web',
                'body': 'testing 123',
                'hint': 'hint123',
                'solution': 'CTF{123}'
            },
            user_id=2)
def setup_third_challenge(app, client):
    challenges_admin.create_challenge()


@setup_test('/api/challenges/3',
            method='POST',
            json={'flag': 'CTF{123}'},
            user_id=1)
def submit_third_challenge(app, client):
    response = challenges.submit_flag(3)
    return response


def test_created_challenge_can_be_solved(app, client):
    setup_third_challenge(app, client)
    response = submit_third_challenge(app, client)
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


@setup_test('/api/admin/challenges/1',
            method='POST',
            json={
                'title': 'The New First Challenge',
                'category': 'cryptozoology',
                'body': 'BIGGER AND BADDER',
                'hint': 'HINTS ARE FER NERDS',
                'solution': 'CTF{S0_MUCH_M0R3_C0MPLIC4T3D}'
            },
            user_id=2)
def test_update_challenge(app, client):
    response = challenges_admin.update_challenge(1)
    assert response.status_code == 200
    assert response.json == {
        'id': 1,
        'title': 'The New First Challenge',
        'category': 'cryptozoology',
        'body': 'BIGGER AND BADDER',
        'hint': 'HINTS ARE FER NERDS',
        'solution': 'CTF{S0_MUCH_M0R3_C0MPLIC4T3D}'
    }
