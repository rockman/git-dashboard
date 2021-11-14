import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY") or "XuTWpRZEazBH9hhtyKZ5uMchxjBtvV8g"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data.sqlite")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "testing.sqlite")


def from_flask_env(flask_env):
    if flask_env == 'testing':
        return TestingConfig()

    return DevelopmentConfig()
