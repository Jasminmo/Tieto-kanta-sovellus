from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from . import get_db
from .models import Messages, Threads
from .forms import MessageForm
from .auth import is_logged_in
from .channels import can_view_channel
from sqlalchemy import func

bp = Blueprint('messages', __name__)
db = get_db()


@bp.route('/threads/<int:thread_id>/send/', methods=('GET', 'POST'))
def send(thread_id):
    if not is_logged_in():
        return render_template('auth/not_authorized.html'), 401

    thread = Threads.query.filter(Threads.id == thread_id).first()
    if thread == None or not can_view_channel(thread.channel):
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
    if message == None or not can_view_channel(message.thread.channel):
        return render_template('auth/404.html'), 404

    if not is_logged_in() or message.sender.id != g.user.id:
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
    if not is_logged_in() or not can_view_channel(message.thread.channel):
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
    results = Messages.query.filter(func.lower(Messages.content).like('%' + query.lower() + '%')).order_by(Messages.send_at).all()
    messages = []
    print(messages)
    for message in results:
        if not can_view_channel(message.thread.channel):
            continue
        messages.append(message)
    return render_template('messages/results.html', messages=messages, search_term=query)


@bp.route('/messages/like/<int:id>', methods=('POST',))
def like(id):
    if not is_logged_in():
        return render_template('auth/not_authorized.html'), 401

    message = Messages.query.filter(Messages.id == id).first()
    if message == None:
        return render_template('auth/404.html'), 404

    if g.user not in message.likes:
        message.likes.append(g.user)
        db.session.add(message)
        db.session.commit()
        flash('You have liked this message!', 'success')
    else:
        flash('You have already liked this message!', 'info')
    return redirect(url_for('threads.view', id=message.thread.id))


@bp.route('/messages/unlike/<int:id>', methods=('POST',))
def unlike(id):
    if not is_logged_in():
        return render_template('auth/not_authorized.html'), 401

    message = Messages.query.filter(Messages.id == id).first()
    if message == None:
        return render_template('auth/404.html'), 404

    if g.user in message.likes:
        message.likes.remove(g.user)
        db.session.add(message)
        db.session.commit()
        flash('You have removed your like from this message!', 'success')
    else:
        flash('You have not liked this message yet!', 'success')
    return redirect(url_for('threads.view', id=message.thread.id))
