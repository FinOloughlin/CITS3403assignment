from app import db
from app.models import *

user1 = User(email = "1@1.com", password = "1")

madlib1 = Madlib(id=1,content="blabla")

placeholder1 = Placeholder(value="noun", madlib=madlib1)
placeholder2 = Placeholder(value="verb", madlib=madlib1)

db.session.add_all([user1,madlib1, placeholder1, placeholder2])
db.session.commit()

