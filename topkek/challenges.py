
from flask import Blueprint, jsonify
from flask_jwt import jwt_required


class Challenge(object):
    def __init__(self, id, title, category, text, solved):
        self.id = id
        self.title = title
        self.category = category
        self.text = text
        self.solved = solved

    def __str__(self):
        return 'Challenge(id="%s",title="%s")' % (self.id, self.title)

    def to_dict(self):
        return {"id": self.id,
                "title": self.title,
                "category": self.category,
                "text": self.text,
                "solved": self.solved}


challenges = [
    Challenge(1, "The First Challenge", "crypto",
              "Just think really hard", True),
    Challenge(2, "The Second Challenge", "reversing",
              "Just think really harder", False)
]

challenge_map = {c.id: c for c in challenges}


blueprint = Blueprint("challenges", __name__, url_prefix="/api/app/users")


@jwt_required
@blueprint.route("/<int:user_id>/challenges")
def get_challenges(user_id):
    print("ALL DEM CHALLENGES ", [c.to_dict() for c in challenges])
    return jsonify([c.to_dict() for c in challenges])


@jwt_required
@blueprint.route("/<int:user_id>/challenge/<int:challenge_id>")
def get_user_by_id(user_id, challenge_id):
    if challenge_id and challenge_id in challenge_map:
        return jsonify(challenge_map[challenge_id].to_dict())
    return "Challenge ID not found", 404


def init_app(app):
    app.register_blueprint(blueprint)
