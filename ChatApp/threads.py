from ChatApp import channels
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from . import get_db
from .models import Messages, Threads
from .forms import NewThreadForm, UpdateThreadForm

bp = Blueprint('threads', __name__, url_prefix='/threads')
db = get_db()


@bp.route('/<int:id>')
def view(id):
    thread = Threads.query.filter(Threads.id == id).first()
    if thread == None:
        return render_template('auth/404.html'), 404
    return render_template('threads/view.html', thread=thread)


@bp.route('/new/<int:channel_id>', methods=('GET', 'POST'))
def new(channel_id):
    if g.user == None:
        return render_template('auth/not_authorized.html'), 401

    form = NewThreadForm(request.form)
    if form.validate_on_submit():
        thread = Threads(title=form.title.data, channel_id=id, creator=g.user)
        db.session.add(thread)
        db.session.commit()

        message = Messages(content=form.content.data, thread=thread, sender=g.user)
        db.session.add(message)
        db.session.commit()

        flash('You created a new thread', 'success')
        return redirect(url_for('.view', id=thread.id))

    return render_template('threads/new.html', form=form)


@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    thread = Threads.query.filter(Threads.id == id).first()
    if thread == None:
        return render_template('auth/404.html'), 404
    if g.user == None or g.user.id != thread.creator.id:
        return render_template('auth/not_authorized.html'), 401

    form = UpdateThreadForm(request.form)
    if request.method == 'GET':
        form.title.data = thread.title
    elif form.validate_on_submit():
        thread.title = form.title.data
        db.session.add(thread)
        db.session.commit()
        return redirect(url_for('.view', id=thread.id))

    return render_template('threads/edit.html', form=form)


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
    return redirect(url_for('channels.view', id=channel_id))

