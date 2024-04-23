from flask import render_template
from app import flaskApp

@flaskApp.route("/")
@flaskApp.route("/home")
def home():
    return render_template('home.html')

@flaskApp.route("/signup")
def Signup():
    return render_template('signUp.html')