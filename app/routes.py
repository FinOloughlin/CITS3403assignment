from flask import render_template, redirect, url_for, request
from app import flaskApp, db
from app.models import *

@flaskApp.route("/")
@flaskApp.route("/home")
def home():
    return render_template('home.html')

@flaskApp.route("/signup")
def Signup():
    return render_template('signUp.html')

@flaskApp.route("/submit", methods=['post'])
def Submit():
    print(request.method)
    print(request.form)
    print("submitted")
    return redirect(location=url_for("home"))