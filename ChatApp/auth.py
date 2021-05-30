import functools

from flask import (
    Blueprint, flash, g, current_app, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('auth', __name__, url_prefix='/auth')

db = None

def set_db(conn):
    global db
    db = conn

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        error = None

        if not firstname:
            error = 'First name is required.'
        elif not lastname:
            error = 'Last name is required.'
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.session.execute(
            'SELECT id FROM users WHERE username = :username', {"username":username}
        ).fetchone() is not None:
            error = f"User {username} is already registered."

        if error is None:
            db.session.execute(
                'INSERT INTO users (firstname, lastname, username, salted_passwd) VALUES (:firstname, :lastname, :username, :salted_passwd)',
                {
                    "firstname": firstname,
                    "lastname": lastname,
                    "username": username,
                    "salted_passwd": generate_password_hash(password)
                })
            db.session.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = db.session.execute(
            'SELECT * FROM users WHERE username = :username', {"username": username}
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['salted_passwd'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')



@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))