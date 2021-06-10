from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from . import get_db
from .models import Channels, Threads

bp = Blueprint('threads', __name__, url_prefix='/threads')
db = get_db()


@bp.route('/<int:id>')
def view_thread(id):
    thread = Threads.query.filter(Threads.id == id).first()
    return render_template('threads/view.html', thread=thread)


@bp.route('/new/<int:channel_id>', methods=('GET', 'POST'))
def new(channel_id):
    if g.user == None:
        return render_template('auth/not_authorized.html'), 401

    if request.method == 'POST':
        title = request.form['title']
        channel = Channels.query.filter(Channels.id == channel_id).first()
        error = None

        if not title:
            error = 'title is required.'
        elif channel is None:
            error = f"Channel {channel_id} is not found."

        if error is None:
            thread = Threads(title=title, channel_id=channel_id, creator=g.user)
            db.session.add(thread)
            db.session.commit()
            return redirect(url_for('.view_thread', id=thread.id))

        flash(error)

    return render_template('threads/new.html')



