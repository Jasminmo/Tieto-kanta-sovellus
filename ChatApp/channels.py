from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from . import get_db
from .models import Channels

bp = Blueprint('channels', __name__, url_prefix='/channels')
db = get_db()


@bp.route('/')
def index():
    channels = Channels.query.all()
    messages = {channel.id: channel.get_messages() for channel in channels}
    message_counts = {channel.id: len(messages[channel.id]) for channel in channels}
    return render_template('channels/index.html', channels=channels, messages=messages, message_counts=message_counts)


@bp.route('/<int:id>')
def view_channel(id):
    channel = Channels.query.filter(Channels.id == id).first()
    return render_template('channels/view.html', channel=channel)


@bp.route('/new', methods=('GET', 'POST'))
def new():
    if g.user == None or not g.user.is_admin:
        return render_template('auth/not_authorized.html'), 401

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['title']
        error = None

        if not title:
            error = 'title is required.'

        if error is None:
            channel = Channels(title=title, description=description, creator=g.user)
            db.session.add(channel)
            db.session.commit()
            return redirect(url_for('.view_channel', id=channel.id))

        flash(error)

    return render_template('channels/new.html')


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    if g.user == None or not g.user.is_admin:
        return render_template('auth/not_authorized.html'), 401

    channel = Channels.query.filter(Channels.id == id).first()
    db.session.delete(channel)
    db.session.commit()
    return redirect(url_for('.index'))

