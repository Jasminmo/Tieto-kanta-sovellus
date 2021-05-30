import click

from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

def get_db():
    if 'db' not in g:
        g.db = db
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

def init_db():
    db = get_db()

    #with current_app.open_resource('schema.sql') as f:
    #    db.executescript(f.read().decode('utf8'))
