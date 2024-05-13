from typing import List
from app import db

class User(db.Model):
    email = db.Column(db.String(100), primary_key=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f'<Student {self.email} {self.password}>'
    
class Madlib(db.Model):
    __tablename__ = 'Madlib'
    content = db.Column(db.String(1000), primary_key=True, nullable=False)

    def __repr__(self) -> str:
        return f'<Madlib {self.content}>'