
import os

from flask import Flask

import config
from app.extensions import db # noqa
from app.extensions import init_extensions


basedir = os.path.abspath(os.path.dirname(__file__))
env_flask_env = os.environ.get("FLASK_ENV")


def create_app(flask_env=env_flask_env):
    app = Flask(__name__)
    app.config.from_object(config.from_flask_env(flask_env))

    init_extensions(app)

    from app.main.views import main
    app.register_blueprint(main)

    return app
