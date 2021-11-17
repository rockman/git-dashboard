
from flask import render_template, Blueprint, request, redirect, url_for, flash

from app import db
from app.models import Repo
from app.main.forms import NewRepoForm


main = Blueprint("main", __name__)


@main.route("/")
def home():
    repos = Repo.query.all()
    return render_template('home.html', repos=repos)


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

