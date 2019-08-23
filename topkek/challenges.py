
from flask import Blueprint, jsonify, request, Response
#from flask_jwt import jwt_required, current_identity
from topkek.database import db
from topkek.models import Challenge, User, Solve
from topkek.auth_headers import admin_jwt_required, app_jwt_required


blueprint = Blueprint("challenges", __name__, url_prefix="/api/app/users")


@blueprint.route("/<int:user_id>/challenges")
# @app_jwt_required
def get_challenges(user_id):
    solves = User.query.filter_by(id=user_id).first().solves
    return jsonify([solve.challenge.serialize(solve=solve) for solve in solves])


INCORRECT = 0
CORRECT = 1
ALREADY_SOLVED = 2


# @app_jwt_required
@blueprint.route("/<int:user_id>/challenges/<int:challenge_id>", methods=['GET', 'POST'])
def submit_flag(user_id, challenge_id):
    solve = Solve.query.filter_by(
        user_id=user_id, challenge_id=challenge_id).first()
    if (request.method == 'GET'):
        return jsonify(solve.challenge.serialize(solve))
    if solve.solved:
        return jsonify({'status': ALREADY_SOLVED})
    flag = request.get_json()['flag']
    print("Submitting flag %s", flag)
    if solve.challenge.solution == flag:
        solve.solved = True
        db.session.commit()
        return jsonify({'status': CORRECT, 'challenge': solve.challenge.serialize(solve)})
    else:
        print("it no match :(")
        return jsonify({'status': INCORRECT})


def init_app(app):
    app.register_blueprint(blueprint)
