from typing import List
from app import db

class User(db.Model):
    email = db.Column(db.String(100), primary_key=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)