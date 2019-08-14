
from flask import Blueprint, jsonify, session
from flask_jwt import jwt_required
from topkek import db
from topkek.auth_headers import admin_jwt_required, app_jwt_required


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


def get_user():
    if session["id"]:
        return get_user_by_id(session["id"])
    return None


def get_user_by_id(id):
    connection = db.get_db()
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
    row = cursor.fetchone()
    print(row)
    if row:
        return User(*row)
    return None


def get_user_by_username(username):
    connection = db.get_db()
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    row = cursor.fetchone()
    print(row)
    if row:
        return User(*row)
    return None


blueprint = Blueprint("users", __name__, url_prefix="/api/app/users")


@app_jwt_required
@blueprint.route("/username/<string:username>")
def get_user_by_username_route(username):
    user = get_user_by_username(username)
    if user:
        return jsonify(user.to_dict())
    return "Username not found", 404


@app_jwt_required
@blueprint.route("/<int:id>")
def get_user_by_id_route(id):
    user = get_user_by_id(id)
    if user:
        return jsonify(user.to_dict())
    return "User ID not found", 404


def init_app(app):
    app.register_blueprint(blueprint)
