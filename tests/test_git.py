
import pathlib
import os.path
import tempfile

import app.git as git


basedir = os.path.abspath(os.path.dirname(__file__))


class TestGitRepoFromPath:

    def test_none(self):
        assert git.repo_from_path(None) is None

    def test_empty(self):
        assert git.repo_from_path('') is None

    def test_bad_directory(self):
        assert git.repo_from_path('/something/that/does/not/exist') is None

    def test_not_git_directory(self):
        assert git.repo_from_path(tempfile.gettempdir()) is None

    def test_git_root(self):
        assert git.repo_from_path(pathlib.Path(basedir).parent)

    def test_git_subdirectory(self):
        assert git.repo_from_path(basedir)
