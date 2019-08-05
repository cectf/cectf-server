
from flask import Blueprint, jsonify
from flask_jwt import jwt_required


class User(object):
    def __init__(self, id, username, password, admin):
        self.id = id
        self.username = username
        self.password = password
        self.admin = admin

    def __str__(self):
        return 'User(id="%s")' % self.id

    def to_dict(self):
        return {"id": self.id,
                "username": self.username,
                "password": self.password,
                "admin": self.admin}


users = [
    User(1, 'a', 'b', False),
    User(2, 'abc', '123', True),
    User(3, 'daniel', 'password', True),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


blueprint = Blueprint("users", __name__, url_prefix="/api/app/users")


def get_user_by_username(username):
    if username and username in username_table:
        return username_table[username]
    return None


def get_user_by_id(id):
    if id and id in userid_table:
        return userid_table[id]
    return None


@jwt_required
@blueprint.route("/username/<string:username>")
def get_user_by_username_route(username):
    user = get_user_by_username(username)
    if user:
        return jsonify(user.to_dict())
    return "Username not found", 404


@jwt_required
@blueprint.route("/<int:id>")
def get_user_by_id_route(id):
    user = get_user_by_id(id)
    if user:
        return jsonify(user.to_dict())
    return "User ID not found", 404


def init_app(app):
    app.register_blueprint(blueprint)
