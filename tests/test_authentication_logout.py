from utils import using_role

@using_role(role='contestant')
def test_logout(app, client):
    # get challenges to verify we are logged in as a contestant
    response = client.get('/api/ctf/challenges')
    assert response.status_code == 200

    response = client.get('/api/auth/logout')
    assert response.status_code == 204

    # get challenges to verify we are no longer logged in as a contestant
    response = client.get('/api/ctf/challenges')
    assert response.status_code == 400

def test_logout_not_logged_in(app, client):
    # get challenges to verify we were never logged in as a contestant
    response = client.get('/api/ctf/challenges')
    assert response.status_code == 400

    response = client.get('/api/auth/logout')
    assert response.status_code == 204

    # get challenges to verify we are still not logged in as a contestant
    response = client.get('/api/ctf/challenges')
    assert response.status_code == 400
