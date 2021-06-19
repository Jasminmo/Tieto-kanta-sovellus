from ChatApp import channels
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from . import get_db
from .models import Messages, Threads
from .forms import MessageForm

bp = Blueprint('messages', __name__)
db = get_db()


@bp.route('/threads/<int:thread_id>/send/', methods=('GET', 'POST'))
def send(thread_id):
    if g.user == None:
        return render_template('auth/not_authorized.html'), 401

    thread = Threads.query.filter(Threads.id == thread_id).first()
    if thread == None:
        return render_template('auth/404.html'), 404

    form = MessageForm(request.form)
    if form.validate_on_submit():
        message = Messages(content=form.content.data, thread=thread, sender=g.user)
        db.session.add(message)
        db.session.commit()

        flash('Your message has been send!', 'success')
        return redirect(url_for('threads.view', id=thread.id))

    return render_template('messages/new.html', action_url=url_for('.new'), form=form)

@bp.route('/messages/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    message = Messages.query.filter(Messages.id == id).first()
    if message == None:
        return render_template('auth/404.html'), 404

    if g.user == None or message.sender.id != g.user.id:
        return render_template('auth/not_authorized.html'), 401

    form = MessageForm(request.form)
    if request.method == 'GET':
        form.content.data = message.content
    elif form.validate_on_submit():
        message.content = form.content.data
        db.session.add(message)
        db.session.commit()

        flash('Your message has been updated!', 'success')
        return redirect(url_for('threads.view', id=message.thread.id))

    return render_template('messages/edit.html', form=form)


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

    flash('Your message has been deleted!', 'success')
    return redirect(url_for('threads.view', id=thread_id))


@bp.route('/search', methods=('GET',))
def search():
    query = request.args["query"]
    messages = Messages.query.filter(Messages.content.like('%' + query + '%')).order_by(Messages.send_at).all()
    return render_template('messages/results.html', messages=messages, search_term=query)
