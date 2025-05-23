import os
from flask import Flask, redirect, url_for
from . import db
from . import auth
from . import dashboard
from . import details
import logging

logger = logging.getLogger("my_app")
logger.setLevel(logging.INFO)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(details.bp)
    app.add_url_rule("/", endpoint="index")
    db.init_app(app)
    return app
