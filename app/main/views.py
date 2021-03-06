
import os.path
from datetime import datetime

from flask import render_template, Blueprint, request, redirect, url_for, flash, abort

import app.git

from app import db
from app.models import Repo
from app.main.forms import AddReposForm, FilterReposForm
from app.main.services import search_and_add_git_repos_from_base_path


main = Blueprint("main", __name__)


@main.route("/")
def home():
    repos = Repo.query.order_by(Repo.path).all()
    total_count = len(repos)
    form = FilterReposForm(request.args, meta=dict(csrf=False))

    if form.filter.data:
        filter = form.filter.data.lower()
        repos = [repo for repo in repos if filter in repo.path.lower()]

    return render_template('home.html', repos=repos, total_count=total_count, form=form)


@main.route('/repos/<int:repo_id>/refresh')
def refreshrepo(repo_id):
    repo = Repo.query.filter_by(id=repo_id).first()
    if not repo:
        return abort(404)

    git_repo = app.git.repo_from_path(repo.path)
    status = git_repo.get_status() if git_repo else 'Not a git repo!'

    repo.update_status(status)
    db.session.add(repo)
    db.session.commit()

    return redirect(url_for('main.home'))


@main.route('/repos/<int:repo_id>/delete', methods=['POST'])
def deleterepo(repo_id):
    repo = Repo.query.filter_by(id=repo_id).first()
    if repo:
        db.session.delete(repo)
        db.session.commit()

        flash(f'Deleted: { repo.path }', 'success')

    return redirect(url_for('main.home'))


@main.route('/repos', methods=['GET', 'POST'])
def addrepos():
    form = AddReposForm()

    if form.validate_on_submit():
        new_repos = search_and_add_git_repos_from_base_path(form.basepath.data)
        number_added = len(new_repos)

        if number_added == 0:
            flash('No new repos were found', 'warning')
        else:
            parts = [f'{number_added} repos added:', '<ul>']

            for new_repo in new_repos:
                parts.append(f'<li>{new_repo}</li>')

            parts.append('</ul>')

            flash('\n'.join(parts), 'success')

        return redirect(url_for('main.home'))

    if form.errors:
        for _, errors in form.errors.items():
            for error in errors:
                flash(f'{error}', 'error')

    return render_template('addrepos.html', form=form)


@main.app_template_filter()
def path_parent(path_string):
    return os.path.dirname(path_string) + os.path.sep


@main.app_template_filter()
def path_last(path_string):
    return os.path.basename(path_string)


@main.app_template_filter()
def last_updated(timestamp):
    diff = (datetime.now() - timestamp).total_seconds()

    if diff < 10:
        return 'a few seconds ago'

    if diff < 60 * 1.5:
        return 'about a minute ago'

    if diff < 5 * 60:
        return 'a few minutes ago'

    if diff < 58 * 60:
        return f'about {int(diff) // 60} minutes ago'

    if diff < 65 * 60:
        return 'about an hour ago'

    if diff < 24 * 60 * 60:
        return f'about {int(diff) // (60 * 60)} hours ago'

    if diff < 24 * 1.2 * 60 * 60:
        return 'about a day ago'

    return 'more than a day ago'
