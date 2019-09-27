from flask_security import utils

from cectf_server import commands
from cectf_server.database import db
from cectf_server.models import Challenge, User, Role


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
            title='Challenge Title',
            category='category',
            body='Challenge Body',
            hint='Challenge Hint',
            solution='CTF{fl4g}',
            solves=[]
        )
        db.session.add(challenge)
        db.session.commit()
        assert len(Challenge.query.all()) == 3

    commands.reset_db()
    with app.app_context():
        assert len(Challenge.query.all()) == 0

    result = cli.invoke(args=['populate-test-data'])

    assert 'Inserted test data.' in result.output
    with app.app_context():
        assert len(Challenge.query.all()) == 2


def test_create_user_command_admin(app, cli):
    result = cli.invoke(args=['create-user',
                              '-u', 'username',
                              '-p', 'password',
                              '-e', 'username@email.com',
                              '-r', 'admin'
                              ])

    assert 'Inserted user username' in result.output
    with app.app_context():
        user = User.query.filter_by(username='username').first()
        assert user.username == 'username'
        assert utils.verify_password('password', user.password)
        assert user.email == 'username@email.com'
        assert user.roles == [Role.query.filter_by(name='admin').first()]


def test_create_user_command_contestant(app, cli):
    result = cli.invoke(args=['create-user',
                              '-u', 'username',
                              '-p', 'password',
                              '-e', 'username@email.com',
                              '-r', 'contestant'
                              ])

    assert 'Inserted user username' in result.output
    with app.app_context():
        user = User.query.filter_by(username='username').first()
        assert user.username == 'username'
        assert utils.verify_password('password', user.password)
        assert user.email == 'username@email.com'
        assert user.roles == [Role.query.filter_by(name='contestant').first()]


def test_create_user_command_blank(app, cli):
    result = cli.invoke(args=['create-user',
                              '-u', 'username',
                              '-p', 'password',
                              '-e', 'username@email.com',
                              '-r', '""'
                              ])

    assert 'Inserted user username' in result.output
    with app.app_context():
        user = User.query.filter_by(username='username').first()
        assert user.username == 'username'
        assert utils.verify_password('password', user.password)
        assert user.email == 'username@email.com'
        assert user.roles == []


def test_delete_user_command(app, cli):
    with app.app_context():
        assert User.query.filter_by(username='a').first() is not None

    result = cli.invoke(args=['delete-user', '-u', 'a'])

    assert 'Deleted user a' in result.output
    with app.app_context():
        assert User.query.filter_by(username='a').first() is None


def test_delete_user_command_not_found(app, cli):
    with app.app_context():
        assert User.query.filter_by(username='a').first() is not None
        assert User.query.filter_by(username='ab').first() is None
        assert User.query.filter_by(username='abc').first() is not None

    result = cli.invoke(args=['delete-user', '-u', 'ab'])

    assert 'User ab not found' in result.output
    with app.app_context():
        assert User.query.filter_by(username='a').first() is not None
        assert User.query.filter_by(username='ab').first() is None
        assert User.query.filter_by(username='abc').first() is not None
