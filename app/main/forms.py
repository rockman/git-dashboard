
from pathlib import Path

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, DataRequired, ValidationError


class AddReposForm(FlaskForm):
    basepath = StringField("Base Path", validators=[
        InputRequired("Base Path is required"),
        DataRequired("Base Path cannot be empty")
    ])

    def validate_basepath(form, field):
        path = Path(field.data).expanduser()
        if not path.exists():
            raise ValidationError("Base Path does not exist")

        if not path.is_dir():
            raise ValidationError("Base Path is not a directory")


class RefreshRepoForm(FlaskForm):
    submit = SubmitField("Refresh")


class DeleteRepoForm(FlaskForm):
    submit = SubmitField("Delete")


class FilterReposForm(FlaskForm):
    filter = StringField("Filter")
