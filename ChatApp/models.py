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


secret_channel_users = db.Table('secret_channel_users',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('channel_id', db.Integer, db.ForeignKey('channels.id'), primary_key=True)
)


class Channels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_secret = db.Column(db.Boolean(), unique=False, nullable=False, default=False)
    secret_users = db.relationship('Users', secondary=secret_channel_users)

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


likes_table = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('message_id', db.Integer, db.ForeignKey('messages.id'), primary_key=True)
)


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

    likes = db.relationship('Users', secondary=likes_table)

    def __repr__(self):
        return '<Messages %r>' % self.content


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

