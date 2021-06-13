from ChatApp import channels
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from . import get_db
from .models import Channels, Messages, Threads

bp = Blueprint('threads', __name__, url_prefix='/threads')
db = get_db()


@bp.route('/<int:id>')
def view_thread(id):
    thread = Threads.query.filter(Threads.id == id).first()
    if thread == None:
        return render_template('auth/404.html'), 404
    return render_template('threads/view.html', thread=thread)


@bp.route('/new/<int:channel_id>', methods=('GET', 'POST'))
def new(channel_id):
    if g.user == None:
        return render_template('auth/not_authorized.html'), 401

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['message']
        channel = Channels.query.filter(Channels.id == channel_id).first()
        error = None

        if not title:
            error = 'title is required.'
        if not content:
            error = 'message is required.'
        if channel is None:
            error = f"Channel {channel_id} is not found."

        if error is None:
            thread = Threads(title=title, channel_id=channel_id, creator=g.user)
            message = Messages(content=content, thread=thread, sender=g.user)
            db.session.add(thread)
            db.session.commit()
            return redirect(url_for('.view_thread', id=thread.id))

        flash(error)

    return render_template('threads/new.html')


@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    thread = Threads.query.filter(Threads.id == id).first()
    if thread == None:
        return render_template('auth/404.html'), 404
    if g.user == None or g.user.id != thread.creator.id:
        return render_template('auth/not_authorized.html'), 401

    if request.method == 'POST':
        title = request.form['title']
        error = None

        if not title:
            error = 'title is required.'

        if error is None:
            thread.title = title
            db.session.add(thread)
            db.session.commit()
            return redirect(url_for('.view_thread', id=thread.id))

        flash(error)

    return render_template('threads/edit.html', thread=thread)


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    thread = Threads.query.filter(Threads.id == id).first()
    if thread == None:
        return render_template('auth/404.html'), 404
    if g.user == None or not (g.user.is_admin or (g.user.id == thread.creator.id)):
        return render_template('auth/not_authorized.html'), 401

    channel_id = thread.channel.id
    db.session.delete(thread)
    db.session.commit()
    return redirect(url_for('channels.view_channel', id=channel_id))

