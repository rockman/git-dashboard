
from app import db


class Repo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(4096), nullable=False)
    status = db.Column(db.Text, nullable=True)
    updated = db.Column(db.DateTime, nullable=True)
