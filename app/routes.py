from flask import render_template, redirect, url_for, request, flash
from app import flaskApp, db
from app.models import User, Madlib, Placeholder
import re

@flaskApp.route("/")
@flaskApp.route("/home")
def home():
    return render_template('home.html')

@flaskApp.route("/signup")
def Signup():
    return render_template('signUp.html')

@flaskApp.route("/create")
def create():
    return render_template('createLib.html')

@flaskApp.route("/register", methods=['POST'])
def Register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

        print(User.query.all())
        print("User registered:", email)
        flash("User registered successfully", "success")

        return redirect(location=url_for("home"))
    
def get_next_id():
    last_id = db.session.query(Madlib.id).order_by(Madlib.id.desc()).first()
    if last_id:
        return last_id[0] + 1
    else:
        return 1
    
@flaskApp.route("/submit", methods=['POST'])
def Submit():
    if request.method =='POST':
        content = request.form.get('content')

        placeholders = re.findall(r'\[(.*?)\]', content)

        print(placeholders)

        next_id = get_next_id()

        madlib = Madlib(id=next_id, content=content)

        for placeholder_value in placeholders:
            placeholder = Placeholder(value=placeholder_value, madlib=madlib)
            madlib.placeholders.append(placeholder)
    
        db.session.add(madlib)
        db.session.commit()

        print(Madlib.query.order_by(Madlib.id.desc()).first())
        flash("Submitted madlib successfully", "success")

        return redirect(location=url_for("home"))