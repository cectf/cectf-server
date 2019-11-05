from decorator import decorator
from data import contestant, admin
from cectf_server import commands


class UserContext:
    def __init__(self, client, role):
        self.client = client
        if role == "contestant":
            self.username = contestant['username']
            self.password = contestant['password']
        if role == "admin":
            self.username = admin['username']
            self.password = admin['password']

    def __enter__(self):
        self.client.post(
            '/api/auth/login',
            json={
                'username': self.username,
                'password': self.password,
                'csrf_token': self.client.csrf_token},
            headers={
                'Accept': 'application/json',
                'Origin': 'http://localhost'}
        )

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.get(
            '/api/auth/logout',
            headers={
                'Accept': 'application/json',
                'Origin': 'http://localhost'}
        )


def role(client, role):
    return UserContext(client, role)


_role = role


def using_role(role):
    @decorator
    def test_decorator(test, app, client, *args, **kwargs):
        with _role(client, role):
            return test(app, client, *args, **kwargs)
    return test_decorator