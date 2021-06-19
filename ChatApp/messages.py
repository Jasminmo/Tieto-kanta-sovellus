from ChatApp import channels
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from . import get_db
from .models import Channels, Messages, Threads

bp = Blueprint('messages', __name__)
db = get_db()


@bp.route('/threads/<int:thread_id>/send/', methods=('GET', 'POST'))
def send(thread_id):
    if g.user == None:
        return render_template('auth/not_authorized.html'), 401

    if request.method == 'POST':
        content = request.form['message']
        thread = Threads.query.filter(Threads.id == thread_id).first()
        if thread == None:
            return render_template('auth/404.html'), 404

        error = None
        if not content:
            error = 'message is required.'

        if error is None:
            message = Messages(content=content, thread=thread, sender=g.user)
            db.session.add(thread)
            db.session.commit()
            return redirect(url_for('threads.view_thread', id=thread.id))

        flash(error)

    return render_template('messages/new.html')

@bp.route('/messages/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    message = Messages.query.filter(Messages.id == id).first()
    if message == None:
        return render_template('auth/404.html'), 404

    if g.user == None or message.sender.id != g.user.id:
        return render_template('auth/not_authorized.html'), 401

    if request.method == 'POST':
        content = request.form['message']

        error = None
        if not content:
            error = 'message is required.'

        if error is None:
            message.content = content
            db.session.add(message)
            db.session.commit()
            return redirect(url_for('threads.view_thread', id=message.thread.id))

        flash(error)

    return render_template('messages/edit.html', message=message)


@bp.route('/messages/delete/<int:id>', methods=('POST',))
def delete(id):
    message = Messages.query.filter(Messages.id == id).first()
    if message == None:
        return render_template('auth/404.html'), 404
    if g.user == None or g.user.id != message.sender.id:
        return render_template('auth/not_authorized.html'), 401

    thread_id = message.thread.id
    db.session.delete(message)
    db.session.commit()
    return redirect(url_for('threads.view_thread', id=thread_id))


@bp.route('/search', methods=('GET',))
def search():
    query = request.args["query"]
    messages = Messages.query.filter(Messages.content.like('%' + query + '%')).order_by(Messages.send_at).all()
    return render_template('messages/results.html', messages=messages, search_term=query)
