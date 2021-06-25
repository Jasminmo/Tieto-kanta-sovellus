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

channel_ratings = db.Table('channel_ratings',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('channel_id', db.Integer, db.ForeignKey('channels.id'), primary_key=True),
    db.Column('rating', db.Integer, nullable=False)
)

class Channels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    is_secret = db.Column(db.Boolean(), unique=False, nullable=False, default=False)
    secret_users = db.relationship('Users', secondary=secret_channel_users)
    raters = db.relationship("Users", secondary=channel_ratings)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creator = db.relationship('Users', backref=db.backref('channels', lazy=True, cascade="all, delete"))

    def rate(self, user, value):
        if user == None:
            return None
        fetch = 'select * from channel_ratings where user_id = :user_id and channel_id = :channel_id'
        result = db.session.execute(fetch, {"user_id": user.id, "channel_id": self.id}).fetchall()
        if len(result) == 0:
            insert = 'insert into channel_ratings (user_id, channel_id, rating) values (:user_id, :channel_id, :value)'
            result = db.session.execute(insert, {"user_id": user.id, "channel_id": self.id, "value": int(value)})
        else:
            insert = 'update channel_ratings set rating=:value where user_id=:user_id and channel_id=:channel_id'
            result = db.session.execute(insert, {"user_id": user.id, "channel_id": self.id, "value": int(value)})

    def ratings(self):
        fetch = 'select round(avg(rating),2) as mean, count(rating) as count from channel_ratings where channel_id = :channel_id'
        result = db.session.execute(fetch, {"channel_id": self.id}).fetchall()[0]
        ratings = {'mean': str(result[0]), 'count': result[1]}
        return ratings
    

    def rating(self, user):
        if user == None:
            return None
        fetch = 'select rating from channel_ratings where channel_id = :channel_id and user_id=:user_id'
        result = db.session.execute(fetch, {"channel_id": self.id, "user_id": user.id}).fetchall()
        if len(result) == 0:
            return None
        rating = result[0][0]
        rating_class = ['','','','','']
        for i in range(rating):
            rating_class[i] = '-fill'
        return rating_class

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
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

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
    send_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sender = db.relationship('Users', backref=db.backref('messages', lazy=True, cascade="all, delete"))

    thread_id = db.Column(db.Integer, db.ForeignKey('threads.id'), nullable=False)
    thread = db.relationship('Threads', backref=db.backref('messages', lazy=True, cascade="all, delete"))

    reply_to_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=True)
    replies = db.relationship('Messages', backref=db.backref('reply_to', remote_side=[id]))

    likes = db.relationship('Users', secondary=likes_table)

    def __repr__(self):
        return '<Messages %r>' % self.content
