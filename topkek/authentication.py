
from topkek import users
from flask import jsonify, session
from werkzeug.security import safe_str_cmp
from flask_jwt import JWT


def authenticate(username, password):
    user = users.get_user_by_username(username)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return users.get_user_by_id(user_id)


def init_app(app):
    jwt = JWT(app, authenticate, identity)
