from app.models import *
from app import db

class UserCreationError(Exception):
    pass

class UserLoginError(Exception):
    pass

def register_user(email, password):

    existing_user = User.query.filter_by(email=email).first()
    if not email or not password:
        raise UserCreationError("Email and password are required")
    
    if existing_user:
        raise UserCreationError("User with this email already exists")
    
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return True

def login_user(email, password):
    if not email or not password:
        raise UserLoginError("Email and password are required")
    
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        # Authentication successful
        return True
    else:
        return False