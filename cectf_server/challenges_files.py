
import os
from flask import Blueprint, jsonify, request, Response, current_app
from flask_security.core import current_user
from flask_security.decorators import login_required, roles_required
from werkzeug.utils import secure_filename
from .database import db
from .models import Challenge, User, Solve

blueprint = Blueprint('challenges_files', __name__,
                      url_prefix='/api/files')


def _get_url(challenge_id, filename):
    return os.path.join(current_app.config['CECTF_FRONTEND_DOMAIN'],
                        str(challenge_id),
                        filename)


@blueprint.route('/<int:challenge_id>', methods=['GET'])
@login_required
def get_challenge_files(challenge_id):
    files_path = os.path.join(current_app.config['CECTF_FILE_LOCATION'],
                              str(challenge_id))
    try:
        files = [{'name': f,
                  'url': _get_url(challenge_id, f)
                  } for f in os.listdir(files_path)]
        return jsonify(files)
    except FileNotFoundError:
        return jsonify([])


@blueprint.route('/<int:challenge_id>', methods=['POST'])
@roles_required('admin')
@login_required
def upload_challenge_file(challenge_id):
    print("ALL DEM FILES", request.files)
    print("ALL DEM FILES", request.files['file'])
    file = request.files['file']
    filename = os.path.basename(file.filename)
    print("SAVING", file, filename)
    try:
        os.makedirs(os.path.join(
            current_app.config['CECTF_FILE_LOCATION'],
            str(challenge_id)))
    except FileExistsError:
        pass
    file.save(os.path.join(current_app.config['CECTF_FILE_LOCATION'],
                           str(challenge_id),
                           filename))
    return jsonify({'name': filename,
                    'url': _get_url(challenge_id, filename)
                    })


@blueprint.route('/<int:challenge_id>/<string:file_name>', methods=['DELETE'])
@roles_required('admin')
@login_required
def delete_challenge_file(challenge_id, file_name):
    try:
        os.remove(os.path.join(current_app.config['CECTF_FILE_LOCATION'],
                               str(challenge_id),
                               file_name))
    except:
        return ('File Not Found', 404)
    return ('', 200)


def init_app(app):
    app.register_blueprint(blueprint)