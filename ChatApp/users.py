from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from . import get_db
from .models import Channels, Threads

bp = Blueprint('mypage', __name__, url_prefix='/my')
db = get_db()


@bp.route('/')
def index():
    return render_template('users/threads.html')


@bp.route('threads')
def threads():
    return render_template('users/threads.html')
