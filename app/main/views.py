
from flask import render_template, Blueprint, request, redirect, url_for, flash

from app import db
from app.models import Repo


main = Blueprint("main", __name__)


@main.route("/")
def home():
    repos = Repo.query.all()
    return render_template('home.html', repos=repos)


@main.route('/add-repo', methods=['GET', 'POST'])
def addrepo():
    if request.method == 'GET':
        return render_template('addrepo.html')

    path = request.form.get('path')
    if not path:
        flash('Path is empty', 'error')
        return redirect(url_for('main.addrepo'))

    if Repo.query.filter_by(path=path).count() > 0:
        flash('Path already exists', 'warning')
        return redirect(url_for('main.addrepo'))

    repo = Repo(path=path)
    db.session.add(repo)
    db.session.commit()

    return redirect(url_for('main.home'))