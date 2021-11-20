
from flask import render_template, Blueprint, request, redirect, url_for, flash, abort

from app import db
from app.models import Repo
from app.main.forms import NewRepoForm, DeleteRepoForm, FilterReposForm


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

    form = DeleteRepoForm()

    return render_template('repo.html', repo=repo, form=form)


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

            repo = Repo(path=form.path.data)
            db.session.add(repo)
            db.session.commit()

            flash(f'Repo added: {repo.path}', 'info')
        
        return redirect(url_for('main.home'))

    if form.errors:
        flash(f'Input has errors', 'error')

    return render_template('addrepo.html', form=form)

