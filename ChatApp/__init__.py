import os
from os import getenv

from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        FLASK_APP=getenv("FLASK_APP"),
        FLASK_ENV=getenv("FLASK_ENV"),
        SQLALCHEMY_DATABASE_URI=getenv("DATABASE_URL"),
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

    # a simple page that says hello
    @app.route('/hello')
    def index():
        return render_template('index.html')

    # database initialization
    #from . import db
    #db.init_app(app)

    db = SQLAlchemy(app)


    # authentication
    from . import auth
    auth.set_db(db)
    app.register_blueprint(auth.bp)

    app.add_url_rule("/", endpoint="index")
    return app
