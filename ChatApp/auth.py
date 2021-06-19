from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from . import get_db
from .forms import UserForm
from .models import Users
from ChatApp import forms

bp = Blueprint('auth', __name__, url_prefix='/auth')
db = get_db()


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = Users.query.filter(Users.id == user_id).first()


@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = UserForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        if db.session.execute('SELECT id FROM users WHERE username = :username', {"username": username}).fetchone() is not None:
            flash(f"User {username} is already registered", 'danger')
            return render_template('auth/register.html', form=form)

        user = Users(username=username, password=generate_password_hash(form.password.data), is_admin=form.is_admin.data)
        db.session.add(user)
        db.session.commit()

        flash('Thanks for registering!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)



@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = UserForm(request.form)
    if form.validate_on_submit():
        user = Users.query.filter(Users.username == form.username.data).first()

        if user is None or not check_password_hash(user.password, form.password.data):
            flash('Incorrect username or password.', 'danger')
        else:
            session.clear()
            session['user_id'] = user.id
            flash('Logged in as ' + user.username + '!', 'info')
            return redirect(url_for('index'))

    return render_template('auth/login.html', form=form)


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    flash('You have logged out!', 'info')
    return redirect(url_for("index"))