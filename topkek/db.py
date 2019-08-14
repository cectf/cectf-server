

import click
import re
from flask import current_app, g
from flask.cli import with_appcontext
import mysql.connector as mariadb


def get_db():
    if not 'db' in g:
        g.db = mariadb.connect(database=current_app.config['DATABASE'])
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def _run_sql(filename):
    db = get_db()
    with current_app.open_resource(filename) as f:
        lines = f.read().decode('utf8').split(';')
        for line in lines:
            line = re.sub('[\r\n]', '', line)
            cursor = db.cursor(buffered=True)
            cursor.execute(line)
            cursor.close()
        db.commit()


def init_db():
    _run_sql('schema.sql')


def init_test_db():
    _run_sql('testdata.sql')


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


@click.command('init-test-db')
@with_appcontext
def init_test_db_command():
    """Put test data into the database"""
    init_test_db()
    click.echo('Inserted test data')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(init_test_db_command)
