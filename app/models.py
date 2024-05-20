from typing import List
from app import db

class User(db.Model):
    email = db.Column(db.String(100), primary_key=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f'<Student {self.email} {self.password}>'
    
class MadLib(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story = db.Column(db.String(1000), nullable=False)
    questions = db.Column(db.String(1000), nullable=False)
    placeholders = db.Column(db.String(1000), nullable=False)