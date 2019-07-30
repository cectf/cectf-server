from datetime import datetime, timedelta
from flask import current_app, jsonify, request
from werkzeug.security import safe_str_cmp
import jwt
from topkek.services import auth_service


def init_app(app):
    auth_url_options = {'methods': ['POST']}
    auth_url_options.setdefault('view_func', _auth_request_handler)
    app.add_url_rule('/auth', **auth_url_options)


def _auth_request_handler():
    print("Received ", request.get_data())
    print("hehehe ", request.content_type)
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)
    criterion = [username, password, len(data) == 2]

    if not all(criterion):
        raise AuthError('Bad Request', 'Invalid credentials')

    user = _authenticate(username, password)

    if user:
        access_token = _get_token_for(user)
        response = jsonify({'access_token': access_token.decode('utf-8')})
        response.set_cookie(key='token', value=access_token)
        return response
    else:
        raise AuthError('Bad Request', 'Invalid credentials')


class AuthError(Exception):
    def __init__(self, error, description, status_code=401, headers=None):
        self.error = error
        self.description = description
        self.status_code = status_code
        self.headers = headers

    def __repr__(self):
        return 'AuthError: %s' % self.error

    def __str__(self):
        return '%s. %s' % (self.error, self.description)
