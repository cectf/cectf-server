
from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required, current_identity
from topkek import db
from topkek.auth_headers import admin_jwt_required, app_jwt_required


class Challenge(object):
    def __init__(self, id, title, category, body, hint, solution, hinted, solved):
        self.id = id
        self.title = title
        self.category = category
        self.body = body
        self.hint = hint
        self.solution = solution
        self.hinted = hinted
        self.solved = solved

    def __str__(self):
        return 'Challenge(id="%s",title="%s")' % (self.id, self.title)

    def to_dict(self):
        _dict = {"id": self.id,
                 "title": self.title,
                 "category": self.category,
                 "body": self.body,
                 "hinted": self.hinted,
                 "solved": self.solved}
        if self.hinted:
            _dict["hint"] = self.hint
        if self.solved:
            _dict["solution"] = self.solution
        return _dict


blueprint = Blueprint("challenges", __name__, url_prefix="/api/app/users")


@blueprint.route("/<int:user_id>/challenges")
@app_jwt_required
def get_challenges(user_id):
    print("yee yee", current_identity)
    connection = db.get_db()
    cursor = connection.cursor(buffered=True)
    cursor.execute(
        "SELECT id, title, category, body, hint, solution, hinted, solved FROM challenges LEFT JOIN solves ON challenges.id = solves.challenge_id")
    return jsonify([Challenge(*c).to_dict() for c in cursor])


@app_jwt_required
@blueprint.route("/<int:user_id>/challenge/<int:challenge_id>", methods=['GET', 'POST'])
def submit_flag(user_id, challenge_id):
    connection = db.get_db()
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT id, title, category, body, hint, solution, hinted, solved FROM challenges LEFT JOIN solves ON challenges.id=solves.challenge_id WHERE challenges.id=%s", (challenge_id,))
    row = cursor.fetchone()
    challenge = Challenge(*row)
    if (request.method == 'GET'):
        return jsonify(challenge.to_dict())

    if challenge.solved:
        return jsonify({'message': 'Already solved!'})
    flag = request.get_json()['flag']
    print("Submitting flag %s", flag)
    if challenge.solution == flag:
        challenge.solved = True
        cursor = connection.cursor(buffered=True)
        cursor.execute("INSERT INTO solves (user_id, challenge_id, hinted, solved) VALUES (%s, %s, %s, %s)",
                       (user_id, challenge_id, challenge.hinted, challenge.solved))
        connection.commit()
        return jsonify(challenge.to_dict())
    else:
        print("it no match :(")
        return jsonify(challenge.to_dict()), 403
    return jsonify(challenge.to_dict())


def init_app(app):
    app.register_blueprint(blueprint)
