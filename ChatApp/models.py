from werkzeug.security import generate_password_hash
from datetime import datetime
from . import get_db

db = get_db()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean(), unique=False, nullable=False, default=False)

    def __repr__(self):
        return '<User %r >' % self.username


class Channels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creator = db.relationship('Users', backref=db.backref('channels', lazy=True, cascade="all, delete"))

    def __repr__(self):
        return '<Channel %r>' % self.title


class Threads(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creator = db.relationship('Users', backref=db.backref('threads', lazy=True, cascade="all, delete"))

    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
    channel = db.relationship('Channels', backref=db.backref('threads', lazy=True, cascade="all, delete"))

    def __repr__(self):
        return '<Threads %r>' % self.title


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True)
    send_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sender = db.relationship('Users', backref=db.backref('messages', lazy=True, cascade="all, delete"))

    thread_id = db.Column(db.Integer, db.ForeignKey('threads.id'), nullable=False)
    thread = db.relationship('Threads', backref=db.backref('messages', lazy=True, cascade="all, delete"))

    reply_to_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=True)
    replies = db.relationship('Messages', backref=db.backref('reply_to', remote_side=[id]))

    def __repr__(self):
        return '<Messages %r>' % self.content


def setup_defaults():
    admin = Users(username='admin', password=generate_password_hash('password'), is_admin=True)
    db.session.add(admin)

    user = Users(username='customer', password=generate_password_hash('password'))
    db.session.add(user)

    default_channel = Channels(title='Default', description="This is default channel.", creator=admin)
    db.session.add(default_channel)

    thread1 = Threads(title='Starting thread', creator=user, channel=default_channel)
    db.session.add(thread1)

    message1 = Messages(content='H1. How are you?', sender=user, thread=thread1)
    db.session.add(message1)

    message2 = Messages(content='H2. I\'m fine.', sender=user, thread=thread1, reply_to=message1)
    db.session.add(message2)

    db.session.commit()

