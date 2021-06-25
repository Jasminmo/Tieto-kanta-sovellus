import click
from flask.cli import with_appcontext
from .models import *

from . import get_db
db = get_db()


def setup_defaults():
    subjects = ['Cinema', 'Viral Stories', 'Memes', 'Hobbies']
    topics = ['Something...', 'What about...', 'Popular']
    admin = Users(username='admin', password=generate_password_hash('password'), is_admin=True)
    db.session.add(admin)

    customer = Users(username='customer', password=generate_password_hash('password'))
    db.session.add(customer)

    user1 = Users(username='user1', password=generate_password_hash('password'))
    db.session.add(user1)

    user2 = Users(username='user2', password=generate_password_hash('password'))
    db.session.add(user2)

    default_channel = Channels(title='Default', description="This is default channel.", creator=admin)
    db.session.add(default_channel)

    secret_channel = Channels(title='Secret', description="This is secret channel.", creator=admin, is_secret=True)
    secret_channel.secret_users.append(user1)
    secret_channel.secret_users.append(user2)
    db.session.add(default_channel)

    for i in range(4):
        new_channel = Channels(title=subjects[i], description='This is a discussion board for the subject ' + subjects[i], creator=admin)
        db.session.add(new_channel)

        for j in range(3):
            thread = Threads(title=topics[j], creator=admin, channel=new_channel)
            db.session.add(thread)

            message = Messages(content='First!', sender=customer, thread=thread)
            db.session.add(message)

            message = Messages(content='Second!', sender=customer, thread=thread, reply_to=message)
            db.session.add(message)

            message = Messages(content='Hi! How are you?', sender=admin, thread=thread)
            db.session.add(message)

            message = Messages(content='Hi! I\'m fine.', sender=customer, thread=thread, reply_to=message)
            db.session.add(message)

    db.session.commit()


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
