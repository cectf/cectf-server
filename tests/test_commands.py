from flask_security import utils

from cectf_server import commands
from cectf_server.database import db
from cectf_server.models import Challenge, User, Role

from cectf_server.test_data import contestant, admin, new_user, challenges


def test_drop_db_command(cli):
    result = cli.invoke(args=['drop-db'])
    assert 'All tables dropped from the database.' in result.output


def test_init_db_command(app, cli):
    commands.drop_db()
    result = cli.invoke(args=['init-db'])
    assert 'All tables and roles added to the database.' in result.output


def test_reset_db_command(app, cli):
    result = cli.invoke(args=['reset-db'])
    assert 'Reset the database.' in result.output
    with app.app_context():
        assert Challenge.query.first() is None


def test_populate_test_data_command(app, cli):
    with app.app_context():
        challenge = Challenge(
            title=challenges[3]['title'],
            category=challenges[3]['category'],
            author=challenges[3]['author'],
            body=challenges[3]['body'],
            solution=challenges[3]['solution'],
            solves=[]
        )
        db.session.add(challenge)
        db.session.commit()
        assert len(Challenge.query.all()) == 4

    commands.reset_db()
    with app.app_context():
        assert len(Challenge.query.all()) == 0

    result = cli.invoke(args=['populate-test-data'])

    assert 'Inserted test data.' in result.output
    with app.app_context():
        assert len(Challenge.query.all()) == 3


def test_create_user_command_admin(app, cli):
    result = cli.invoke(args=['create-user',
                              '-u', new_user['username'],
                              '-p', new_user['password'],
                              '-e', new_user['email'],
                              '-r', 'admin'
                              ])

    assert 'Inserted user ' + new_user['username'] in result.output
    with app.app_context():
        user = User.query.filter_by(username=new_user['username']).first()
        assert user.username == new_user['username']
        assert utils.verify_password(new_user['password'], user.password)
        assert user.email == new_user['email']
        assert user.roles == [Role.query.filter_by(name='admin').first()]


def test_create_user_command_contestant(app, cli):
    result = cli.invoke(args=['create-user',
                              '-u', new_user['username'],
                              '-p', new_user['password'],
                              '-e', new_user['email'],
                              '-r', 'contestant'
                              ])

    assert 'Inserted user ' + new_user['username'] in result.output
    with app.app_context():
        user = User.query.filter_by(username=new_user['username']).first()
        assert user.username == new_user['username']
        assert utils.verify_password(new_user['password'], user.password)
        assert user.email == new_user['email']
        assert user.roles == [Role.query.filter_by(name='contestant').first()]


def test_create_user_command_blank(app, cli):
    result = cli.invoke(args=['create-user',
                              '-u', new_user['username'],
                              '-p', new_user['password'],
                              '-e', new_user['email'],
                              '-r', '""'
                              ])

    assert 'Inserted user ' + new_user['username'] in result.output
    with app.app_context():
        user = User.query.filter_by(username=new_user['username']).first()
        assert user.username == new_user['username']
        assert utils.verify_password(new_user['password'], user.password)
        assert user.email == new_user['email']
        assert user.roles == []


def test_delete_user_command(app, cli):
    with app.app_context():
        assert User.query.filter_by(
            username=contestant['username']).first() is not None

    result = cli.invoke(args=['delete-user', '-u', contestant['username']])

    assert 'Deleted user ' + contestant['username'] in result.output
    with app.app_context():
        assert User.query.filter_by(
            username=contestant['username']).first() is None


def test_delete_user_command_not_found(app, cli):
    with app.app_context():
        assert User.query.filter_by(
            username=contestant['username']).first() is not None
        assert User.query.filter_by(
            username=admin['username']).first() is not None
        assert User.query.filter_by(
            username=new_user['username']).first() is None

    result = cli.invoke(args=['delete-user', '-u', new_user['username']])

    assert 'User ' + new_user['username'] + ' not found' in result.output
    with app.app_context():
        assert User.query.filter_by(
            username=contestant['username']).first() is not None
        assert User.query.filter_by(
            username=admin['username']).first() is not None
        assert User.query.filter_by(
            username=new_user['username']).first() is None
