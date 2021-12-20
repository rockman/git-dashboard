
import os.path

from flask import render_template, Blueprint, request, redirect, url_for, flash, abort

import app.git

from app import db
from app.models import Repo
from app.main.forms import AddReposForm, DeleteRepoForm, FilterReposForm, RefreshRepoForm
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


@main.route('/repos/<int:repo_id>')
def viewrepo(repo_id):
    repo = Repo.query.filter_by(id=repo_id).first()
    if not repo:
        return abort(404)

    refresh_form = RefreshRepoForm()
    delete_form = DeleteRepoForm()

    return render_template('repo.html', repo=repo, refresh_form=refresh_form, delete_form=delete_form)


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

    return redirect(url_for('main.viewrepo', repo_id=repo_id))


@main.route('/repos/<int:repo_id>', methods=['POST'])
def deleterepo(repo_id):
    repo = Repo.query.filter_by(id=repo_id).first()
    if repo:
        db.session.delete(repo)
        db.session.commit()

        flash(f'Deleted: { repo.path }', 'success')

    return redirect(url_for('main.home'))


@main.route('/add-repos', methods=['GET', 'POST'])
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
