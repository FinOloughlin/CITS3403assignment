from flask import render_template, redirect, url_for, request, flash
from app import flaskApp, db
from app.models import User, Madlib

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
    
@flaskApp.route("/submit", methods=['POST'])
def Submit():
    if request.method =='POST':
        content = request.form.get('content')
    
        game = Madlib(content=content)
        db.session.add(game)
        db.session.commit()

        print(Madlib.query.all())
        flash("Submitted madlib successfully", "success")

        return redirect(location=url_for("home"))