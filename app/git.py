

import os
import subprocess
from pathlib import Path


class Repo:

    def __init__(self, path):
        self.path = path
        self.status = None

    def get_status(self):
        self.status = self._get_status()
        return self.status

    def _get_status(self):
        path = Path(self.path)
        if not path.exists:
            return 'Path does not exist!'

        p = _run_fetch(path)
        if p.returncode != 0:
            return 'Could not fetch!'

        p = _run_status(path)
        if p.returncode != 0:
            return 'Could not get status!'

        return p.stdout.decode('ascii')


def repo_from_path(path_string):
    if path_string is None or not path_string:
        return None

    path = Path(path_string)

    if path.exists:
        p = _run_rev_parse(path)
        if p.returncode == 0:
            return Repo(p.stdout.decode('ascii').strip())

    return None


def find_repos_from_path(base_path_string):
    repo = repo_from_path(base_path_string)
    if repo is not None:
        return [repo]

    repos = []
    path = Path(base_path_string).expanduser().absolute()

    for root, dirs, files in os.walk(str(path)):
        if '.git' in dirs:
            repo = repo_from_path(root)
            if repo is not None:
                repos.append(repo)

    return repos


def _run_rev_parse(path):
    return subprocess.run(_rev_parse(path), capture_output=True)


def _run_status(path):
    return subprocess.run(_status(path), capture_output=True)


def _run_fetch(path):
    return subprocess.run(_fetch(path), capture_output=True)


def _args(path, *args):
    return ['git', '-C', path.resolve()] + list(args)


def _rev_parse(path):
    return _args(path, 'rev-parse', '--show-toplevel')


def _status(path):
    return _args(path, 'status', '-sb')


def _fetch(path):
    return _args(path, 'fetch', '--all', '--prune')
