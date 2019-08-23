import os
from flask import Flask
from flask_security import Security


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='mysql+pymysql://localhost/test',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_AUTH_URL_RULE='/api/login/auth'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import database
    database.init_app(app)

    # Setup Flask-Security
    security = Security(app, database.user_datastore)

    from . import users
    users.init_app(app)

    from . import challenges
    challenges.init_app(app)

    #from . import authentication
    # authentication.init_app(app)

    return app
