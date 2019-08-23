
from flask import Blueprint, jsonify, session
from topkek.database import db
from topkek.models import User
#from topkek.auth_headers import admin_jwt_required, app_jwt_required

'''
class User(object):
    def __init__(self, id, username, password, admin):
        self.id = id
        self.username = username
        self.password = password
        self.admin = True if admin else False

    def __str__(self):
        return 'User(id="%s")' % self.id

    def to_dict(self):
        return {"id": self.id,
                "username": self.username,
                "password": self.password,
                "admin": self.admin}
'''


def get_user():
    if session["id"]:
        return get_user_by_id(session["id"])
    return None


def get_user_by_id(id):
    return User.query.filter_by(id=id).first()


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


blueprint = Blueprint("users", __name__, url_prefix="/api/app/users")


# @app_jwt_required
@blueprint.route("/username/<string:username>")
def get_user_by_username_route(username):
    user = get_user_by_username(username)
    if user:
        return jsonify(user.serialize)
    return "Username not found", 404


# @app_jwt_required
@blueprint.route("/<int:id>")
def get_user_by_id_route(id):
    user = get_user_by_id(id)
    if user:
        return jsonify(user.serialize)
    return "User ID not found", 404


def init_app(app):
    app.register_blueprint(blueprint)
