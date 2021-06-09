import click
from flask.cli import with_appcontext
from .models import setup_defaults

from . import get_db
db = get_db()


def init_db():
    """Drop and create tables."""
    #db.drop_all()
    db.create_all()
    setup_defaults()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Drop and create tables."""
    init_db()
    click.echo("The database is now initialized.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.cli.add_command(init_db_command)
