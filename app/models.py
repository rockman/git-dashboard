
from sqlalchemy.orm import validates

from app import db


class Repo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(4096), nullable=False)
    status = db.Column(db.Text, nullable=True)
    updated = db.Column(db.DateTime, nullable=True)

    @validates('path')
    def validate_path(self, key, value):
        if not value or not value.strip():
            raise ValueError('path cannot be empty')
        return value
