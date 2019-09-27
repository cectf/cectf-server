from decorator import decorator


class UserContext:
    def __init__(self, client, role):
        self.client = client
        if role == "contestant":
            self.username = "a"
            self.password = "b"
        if role == "admin":
            self.username = "abc"
            self.password = "123"

    def __enter__(self):
        response = self.client.post(
            '/api/login',
            data={
                'username': self.username,
                'password': self.password,
                'csrf_token': self.client.csrf_token},
            headers={
                'Accept': 'application/json',
                'Origin': 'http://localhost'}
        )

    def __exit__(self, exc_type, exc_value, traceback):
        response = self.client.get(
            '/api/logout',
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
