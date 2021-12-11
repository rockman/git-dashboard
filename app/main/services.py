
from app import db
from app.git import find_repos_from_path
from app.models import Repo


def search_and_add_git_repos_from_base_path(base_path_string):
    repos = find_repos_from_path(base_path_string)
    if not repos:
        return 0

    new_repos = [Repo(path=i.path) for i in repos if not Repo.repo_exists(i.path)]
    for repo in new_repos:
        db.session.add(repo)

    db.session.commit()
    return len(new_repos)
