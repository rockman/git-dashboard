
from types import SimpleNamespace

import pytest

from app import create_app, db
from app.models import Repo


context = SimpleNamespace()


def setup_module():
    app = create_app('testing')
    context.app_context = app.app_context()
    context.app_context.push()
    context.app_test_client = app.test_client()
    db.create_all()


def teardown_module():
    db.session.remove()
    db.drop_all()
    context.app_context.pop()


def test_repo_creation():
    repo = Repo(path='/some/path/to/repo')
    db.session.add(repo)
    db.session.commit()

    x = Repo.query.filter_by(path='/some/path/to/repo').first()
    assert x.id == repo.id


def test_repo_path_validation():
    with pytest.raises(ValueError):
        Repo(path='')
