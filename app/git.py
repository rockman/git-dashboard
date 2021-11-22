

import subprocess
from pathlib import Path
from typing import Type



class Repo:

    def __init__(self, path):
        self.path = path
        self.status = None

    def get_status(self):
        path = Path(self.path)
        if not path.exists:
            self.status = 'Path does not exist!'
        else:

            p = _run_status(path)
            if p.returncode == 0:
                self.status = p.stdout.decode('ascii')

            else:
                self.status = 'Could not get status!'

        return self.status


def repo_from_path(path_string):
    if path_string is None or not path_string:
        return None

    path = Path(path_string)

    if path.exists:
        p = _run_rev_parse(path)
        if p.returncode == 0:
            return Repo(p.stdout.decode('ascii').strip())

    return None


def _run_rev_parse(path):
    return subprocess.run(_rev_parse(path), capture_output=True)


def _run_status(path):
    return subprocess.run(_status(path), capture_output=True)


def _rev_parse(path):
    return ['git', '-C', path.resolve(), 'rev-parse', '--show-toplevel']


def _status(path):
    return ['git', '-C', path.resolve(), 'status']
