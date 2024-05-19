from random import randint
from flask import render_template, redirect, url_for, request, flash, session, get_flashed_messages
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
    if not session.get('user_email'):
        return redirect(url_for('home'))
    return render_template('createLib.html')

@flaskApp.route("/play")
def play():
    if not session.get('user_email'):
        return redirect(url_for('home'))

@flaskApp.route("/rules")
def rules():
    return render_template('rules.html')
    
    madlib_count = Madlib.query.count()
    if madlib_count == 0:
        return "No Madlibs available"

    random_id = randint(1, madlib_count)
    madlib = Madlib.query.get(random_id)

    placeholders = [placeholder.value for placeholder in madlib.placeholders]
    placeholder_count = len(madlib.placeholders)

    return render_template('play.html', madlib=madlib,placeholders=placeholders, placeholder_count=placeholder_count)

@flaskApp.route("/register", methods=['POST']) 
def Register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user: # User exists, check password
            if user.password == password:
                session['user_email'] = user.email
                print("logged in:", email)
                return redirect(location=url_for("home"))
            else: #password does not match
                flash("Invalid password for existing email address", "register")
                return redirect(location=url_for("Signup"))
            
        else: # User does not exist, create a new user
            new_user=User(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            session['user_email'] = new_user.email

            print(User.query.all())
            print("User registered:", email)

        return redirect(location=url_for("home"))

@flaskApp.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('home'))
    
def get_next_id(): # to provide unique incrementing ids to the madlibs
    last_id = db.session.query(Madlib.id).order_by(Madlib.id.desc()).first()
    if last_id:
        return last_id[0] + 1
    else:
        return 1
    
@flaskApp.route("/submit", methods=['POST']) #submit madlib
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

        return redirect(location=url_for("home"))
