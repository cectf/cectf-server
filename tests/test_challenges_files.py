import os

from helpers import using_role


def write_file(app, challenge_id, file_name, file_contents):
    try:
        os.makedirs(os.path.join(
            app.config['CECTF_FILE_LOCATION'],
            str(challenge_id)))
    except FileExistsError:
        pass
    with open(os.path.join(
            app.config['CECTF_FILE_LOCATION'],
            str(challenge_id),
            file_name), 'w') as f:
        f.write(file_contents)


def write_tmp_file(app, file_name, file_contents):
    try:
        os.makedirs(os.path.join(
            app.config['CECTF_FILE_LOCATION'],
            'tmp'))
    except FileExistsError:
        pass
    with open(os.path.join(
            app.config['CECTF_FILE_LOCATION'],
            'tmp',
            file_name), 'w') as f:
        f.write(file_contents)
    return open(os.path.join(
        app.config['CECTF_FILE_LOCATION'],
        'tmp',
        file_name), 'rb')


def get_url(app, challenge_id, file_name):
    return os.path.join(
        'files',
        str(challenge_id),
        file_name)


@using_role(role="contestant")
def test_get_challenge_files(app, client):
    write_file(app, 1, 'zippy.zip', 'Not really a zip file!')
    write_file(app, 1, 'hello.txt', 'Hello!')
    write_file(app, 1, 'hello.py', "print('Hello!')")
    write_file(app, 2, 'nope.txt', 'Should not be included!')

    response = client.get('/api/files/1')

    assert response.status_code == 200
    assert response.json == [
        {'name': 'hello.py', 'url': get_url(app, 1, 'hello.py')},
        {'name': 'hello.txt', 'url': get_url(app, 1, 'hello.txt')},
        {'name': 'zippy.zip', 'url': get_url(app, 1, 'zippy.zip')}
    ]


@using_role(role="contestant")
def test_get_challenge_files_challenge_does_not_exist(app, client):
    write_file(app, 1, 'hello.py', "print('Hello!')")

    response = client.get('/api/files/123')

    assert response.status_code == 200
    assert response.json == []


@using_role(role='admin')
def test_upload_challenge_file(app, client):
    with write_tmp_file(app, 'hello.py', "print('Hello!')") as f:
        response = client.post('/api/files/1', data={'file': f})

    assert response.status_code == 200
    assert response.json == {'name': 'hello.py',
                             'url': get_url(app, 1, 'hello.py')}

    response = client.get('/api/files/1')

    assert response.status_code == 200
    assert response.json == [
        {'name': 'hello.py', 'url': get_url(app, 1, 'hello.py')}
    ]


@using_role(role='admin')
def test_upload_two_challenge_files(app, client):
    with write_tmp_file(app, 'hello.py', "print('Hello!')") as f:
        response = client.post('/api/files/1', data={'file': f})

        assert response.status_code == 200
        assert response.json == {'name': 'hello.py',
                                 'url': get_url(app, 1, 'hello.py')}

    with write_tmp_file(app, 'hello.txt', 'Hello!') as f:
        response = client.post('/api/files/1', data={'file': f})

        assert response.status_code == 200
        assert response.json == {'name': 'hello.txt',
                                 'url': get_url(app, 1, 'hello.txt')}

    response = client.get('/api/files/1')

    assert response.status_code == 200
    assert response.json == [
        {'name': 'hello.py', 'url': get_url(app, 1, 'hello.py')},
        {'name': 'hello.txt', 'url': get_url(app, 1, 'hello.txt')}
    ]


@using_role(role='admin')
def test_delete_challenge_file(app, client):
    write_file(app, 1, 'hello.py', "print('Hello!')")

    response = client.delete('/api/files/1/hello.py')
    assert response.status_code == 200

    response = client.get('/api/files/1')

    assert response.status_code == 200
    assert response.json == []


@using_role(role='admin')
def test_delete_challenge_file_does_not_exist(app, client):
    response = client.delete('/api/files/1/hello.py')
    assert response.status_code == 404
