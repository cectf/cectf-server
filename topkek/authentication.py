'''
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
'''

from flask import Blueprint, session, jsonify
from flask_login import current_user
from flask_security.utils import logout_user
from flask_wtf.csrf import generate_csrf

blueprint = Blueprint('authentication', __name__, url_prefix='/api')


# @app_jwt_required
@blueprint.route('/csrf', methods=['GET'])
def csrf():
    return jsonify({'csrf_token': generate_csrf()})


@blueprint.route('/logout', methods=['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
    return ('', 204)


def init_app(app):
    app.register_blueprint(blueprint)
