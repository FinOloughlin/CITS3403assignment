from app import db
from app.models import *

user1 = User(email = "1@1.com", password = "1")

db.session.add_all([user1])
db.session.commit()