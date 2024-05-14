from typing import List
from app import db

class User(db.Model):
    email = db.Column(db.String(100), primary_key=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f'<Student {self.email} {self.password}>'
    
class Madlib(db.Model):
    __tablename__ = 'Madlib'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)

    placeholders = db.relationship('Placeholder', back_populates='madlib')

    def __repr__(self) -> str:
        return f'<Madlib id = "{self.id}", content = "{self.content}", placeholders = "{self.placeholders}">'
    
class Placeholder(db.Model):
    __tablename__ = 'Placeholder'
    id = db.Column(db.Integer, primary_key=True)
    madlib_id = db.Column(db.Integer, db.ForeignKey('Madlib.id'))
    value = db.Column(db.String(255))

    madlib = db.relationship('Madlib', back_populates='placeholders')

    def __repr__(self) -> str:
        return f'<{self.value}>'
