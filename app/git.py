

import subprocess
from pathlib import Path
from typing import Type



class Repo:

    def __init__(self, path):
        self.path = path


def repo_from_path(path_string):
    if path_string is None or not path_string:
        return None

    path = Path(path_string)

    if path.exists:
        p = subprocess.run(_rev_parse(path_string), capture_output=True)
        if p.returncode == 0:
            return Repo(p.stdout.decode('ascii').strip())

    return None


def _rev_parse(path_string):
    return ['git', '-C', path_string, 'rev-parse', '--show-toplevel']

