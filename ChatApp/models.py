from re import S
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

    def get_messages(self):
        messages = []
        for thread in self.threads:
            messages += thread.messages
        return messages


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

    customer = Users(username='customer', password=generate_password_hash('password'))
    db.session.add(customer)

    default_channel = Channels(title='Default', description="This is default channel.", creator=admin)
    db.session.add(default_channel)

    for i in range(3):
        new_channel = Channels(title='Channel ' + str(i+1), description='This is channel number ' + str(i+1), creator=admin)
        db.session.add(new_channel)

        for j in range(4):
            thread = Threads(title='Thread ' + str(j+1), creator=admin, channel=new_channel)
            db.session.add(thread)

            starting_message = Messages(content='This is staring message of this thread.', sender=customer, thread=thread)
            db.session.add(starting_message)

            message1 = Messages(content='Hi! How are you?', sender=admin, thread=thread)
            db.session.add(message1)

            message2 = Messages(content='Hi! I\'m fine.', sender=customer, thread=thread, reply_to=message1)
            db.session.add(message2)

    db.session.commit()

