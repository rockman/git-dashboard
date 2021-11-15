
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class NewRepoForm(FlaskForm):
    path = StringField("Path")
    submit = SubmitField("Add Repo")
