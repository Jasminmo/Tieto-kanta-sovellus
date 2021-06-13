import os
from os import getenv

from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

SQL = None


def get_db():
    return SQL


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        FLASK_APP=getenv("FLASK_APP"),
        FLASK_ENV=getenv("FLASK_ENV"),
        # Fix URI convention used by heroku
        SQLALCHEMY_DATABASE_URI=getenv("DATABASE_URL").replace("postgres://", "postgresql://"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    global SQL
    SQL = SQLAlchemy(app)

    # authentication
    from . import auth, init_db
    init_db.init_app(app)
    app.register_blueprint(auth.bp)

    # channels
    from . import channels
    app.register_blueprint(channels.bp)

    # threads
    from . import threads
    app.register_blueprint(threads.bp)

    # mypage
    from . import users
    app.register_blueprint(users.bp)

    # messages
    from . import messages
    app.register_blueprint(messages.bp)

    app.add_url_rule("/", endpoint="index", view_func=channels.index)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('auth/404.html'), 404

    @app.template_filter('timeformat')
    def _jinja2_filter_datetime(date, format=None):
        if format == None:
            format='%a %h %d %Y %H:%M'
        return date.strftime(format)

    return app
