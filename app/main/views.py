
from flask import render_template, Blueprint, request, redirect, url_for, flash, abort

import app.git

from app import db
from app.models import Repo
from app.main.forms import NewRepoForm, DeleteRepoForm, FilterReposForm, RefreshRepoForm


main = Blueprint("main", __name__)


@main.route("/")
def home():
    repos = Repo.query.all()
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

        flash(f'Repo { repo.path } deleted', 'info')

    return redirect(url_for('main.home'))


@main.route('/add-repo', methods=['GET', 'POST'])
def addrepo():
    form = NewRepoForm()

    if form.validate_on_submit():
        
        if Repo.query.filter_by(path=form.path.data).count() > 0:
            flash('Path already exists', 'warning')

        else:

            path = form.path.data
            git_repo = app.git.repo_from_path(path)

            if git_repo:
                path = git_repo.path

            repo = Repo(path=path)
            db.session.add(repo)
            db.session.commit()

            flash(f'Repo added: {repo.path}', 'info')
        
        return redirect(url_for('main.home'))

    if form.errors:
        flash(f'Input has errors', 'error')

    return render_template('addrepo.html', form=form)

