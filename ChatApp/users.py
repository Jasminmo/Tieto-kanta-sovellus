from flask import Blueprint, render_template
from . import get_db

bp = Blueprint('mypage', __name__, url_prefix='/my')
db = get_db()


@bp.route('/')
def index():
    return render_template('users/threads.html')


@bp.route('threads')
def threads():
    return render_template('users/threads.html')
