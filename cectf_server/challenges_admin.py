
from flask import Blueprint, jsonify, request, Response
from flask_security.core import current_user
from flask_security.decorators import login_required, roles_required
from .database import db
from .models import Challenge, User, Solve


blueprint = Blueprint('challenges_admin', __name__, url_prefix='/api/admin')


@blueprint.route('/challenges')
@roles_required('admin')
@login_required
def get_challenges():
    challenges = Challenge.query.all()
    return jsonify([challenge.serialize() for challenge in challenges])


@blueprint.route('/challenges', methods=['POST'])
@roles_required('admin')
@login_required
def create_challenge():
    challenge = Challenge(
        title=request.json['title'],
        category=request.json['category'],
        body=request.json['body'],
        hint=request.json['hint'],
        solution=request.json['solution'],
        solves=[Solve(
            hinted=False,
            solved=False,
            user=user)
            for user in User.query.all()]
    )
    db.session.add(challenge)
    db.session.commit()
    return jsonify(challenge.serialize())


@blueprint.route('/challenges/<int:challenge_id>', methods=['POST'])
@roles_required('admin')
@login_required
def update_challenge(challenge_id):
    challenge = Challenge.query.filter_by(id=challenge_id).first()
    if request.json['title']:
        challenge.title = request.json['title']
    if request.json['category']:
        challenge.category = request.json['category']
    if request.json['body']:
        challenge.body = request.json['body']
    if request.json['hint']:
        challenge.hint = request.json['hint']
    if request.json['solution']:
        challenge.solution = request.json['solution']
    db.session.commit()
    return jsonify(challenge.serialize())


def init_app(app):
    app.register_blueprint(blueprint)
