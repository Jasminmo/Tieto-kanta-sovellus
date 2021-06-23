from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from . import get_db
from .models import Channels, Users
from .forms import ChannelForm, ChannelSettingsForm
from .auth import is_admin, is_logged_in

bp = Blueprint('channels', __name__, url_prefix='/channels')
db = get_db()


def can_view_channel(channel):
    if channel == None:
        return False
    if is_admin() or not channel.is_secret:
        return True
    if not is_logged_in():
        return False
    user_ids = list(map(lambda u: u.id, channel.secret_users))
    return is_logged_in() and g.user.id in user_ids


@bp.route('/')
def index():
    channels = []
    messages = {}
    message_counts = {}
    for channel in Channels.query.all():
        if not can_view_channel(channel):
            continue
        channels.append(channel)
        messages[channel.id] = channel.get_messages()
        message_counts[channel.id] = len(messages[channel.id])

    return render_template('channels/index.html', channels=channels, messages=messages, message_counts=message_counts)


@bp.route('/<int:id>')
def view(id):
    channel = Channels.query.filter(Channels.id == id).first()
    if not can_view_channel(channel):
        return render_template('auth/404.html'), 404
    return render_template('channels/view.html', channel=channel)


@bp.route('/new', methods=('GET', 'POST'))
def new():
    if not is_admin():
        return render_template('auth/not_authorized.html'), 401

    form = ChannelForm(request.form)
    if form.validate_on_submit():
        channel = Channels(title=form.title.data, description=form.description.data, is_secret=form.is_secret.data, creator=g.user)
        db.session.add(channel)
        db.session.commit()

        flash('Created a new channel!', 'success')
        return redirect(url_for('.view', id=channel.id))

    return render_template('channels/new.html', action_url=url_for('.new'), form=form)


@bp.route('/<int:id>/edit', methods=('POST','GET'))
def edit(id):
    if not is_admin():
        return render_template('auth/not_authorized.html'), 401

    channel = Channels.query.filter(Channels.id == id).first()
    if channel == None:
        return render_template('auth/404.html'), 404

    form = ChannelForm(request.form)
    if request.method == 'GET':
        form.title.data = channel.title
        form.description.data = channel.description
        form.is_secret.data = channel.is_secret
    if form.validate_on_submit():
        channel.title = form.title.data
        channel.description = form.description.data
        db.session.add(channel)
        db.session.commit()

        flash('The channel has been updated!', 'success')
        return redirect(url_for('.view', id=channel.id))

    return render_template('channels/edit.html', form=form, action_url=url_for('.edit', id=id), is_edit=True)


@bp.route('/<int:id>/settings', methods=('POST','GET'))
def settings(id):
    if not is_admin():
        return render_template('auth/not_authorized.html'), 401

    form = ChannelSettingsForm(request.form)
    channel = Channels.query.filter(Channels.id == id).first()
    if channel == None:
        return render_template('auth/404.html'), 404

    return render_template('channels/settings.html', form=form, channel=channel, action_url=url_for('.settings', id=id))


@bp.route('/<int:id>/add-user', methods=('POST','GET'))
def add_user_to_list(id):
    if not is_admin():
        return render_template('auth/not_authorized.html'), 401

    channel = Channels.query.filter(Channels.id == id).first()
    if channel == None:
        return render_template('auth/404.html'), 404

    form = ChannelSettingsForm(request.form)
    if form.validate_on_submit():
        user = Users.query.filter(Users.username == form.username.data).first()
        if user == None:
            form.username.errors.append("Username not found!")
        elif user.is_admin:
            form.username.errors.append("The user " + user.username + " is admin!")
        else:
            channel.secret_users.append(user)
            db.session.add(channel)
            db.session.commit()
            flash('The user has been added to channel list!', 'success')
            return redirect(url_for('.settings', id=id))
    return render_template('channels/settings.html', form=form, channel=channel, action_url=url_for('.settings', id=id))


@bp.route('/<int:channel_id>/remove-user/<int:user_id>', methods=('POST','GET'))
def remove_user_from_list(channel_id, user_id):
    if not is_admin():
        return render_template('auth/not_authorized.html'), 401

    channel = Channels.query.filter(Channels.id == channel_id).first()
    if channel == None:
        return render_template('auth/404.html'), 404

    user = Users.query.filter(Users.id == user_id).first()
    if user == None:
        return render_template('auth/404.html'), 404

    channel.secret_users.remove(user)
    db.session.add(channel)
    db.session.commit()
    flash('The user has been removed from channel list!', 'success')
    return redirect(url_for('.settings', id=channel_id))


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    if not is_admin():
        return render_template('auth/not_authorized.html'), 401

    channel = Channels.query.filter(Channels.id == id).first()
    db.session.delete(channel)
    db.session.commit()

    flash('Deleted channel!', 'success')
    return redirect(url_for('.index'))

