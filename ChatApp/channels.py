from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from . import get_db
from .models import Channels

bp = Blueprint('channels', __name__, url_prefix='/channels')
db = get_db()


@bp.route('/')
def index():
    channels = Channels.query.all()
    return render_template('channels/index.html', channels=channels)


@bp.route('/<int:id>')
def view_channel(id):
    channel = Channels.query.filter(Channels.id == id).first()
    return render_template('channels/view.html', channel=channel)
