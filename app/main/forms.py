
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, DataRequired


class NewRepoForm(FlaskForm):
    path = StringField("Path", validators=[InputRequired("Path required"), DataRequired("Path cannot be empty")])
    submit = SubmitField("Add Repo")


class DeleteRepoForm(FlaskForm):
    submit = SubmitField("Delete Repo")


class FilterReposForm(FlaskForm):
    filter = StringField("Filter")
    submit = SubmitField("Filter Repos")
