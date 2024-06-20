#!/usr/bin/python3
"""
Contains:
    Functions
    =========
    Route handlers for the application
"""
from flask import flash, redirect, render_template, url_for
from flask_login import login_user
from flask_bcrypt import Bcrypt

from flask_app.dynamic.views import app_views
from flask_app.dynamic.forms.login import LoginForm
from flask_app.dynamic.forms.register import RegisterCustomerForm, RegisterDriverForm, RegisterOwnerForm

from models import db
from models.customer import Customer
from models.driver import Driver
from models.owner import Owner
from models.user import User


bcrypt = Bcrypt()

def encrypt_password(password):
    """Encrypts user submitted password using bcrypt"""
    return (bcrypt.generate_password_hash(password).decode("utf-8"))

def check_password(encrypted, password):
    """Checks that a user submitted password at login is correct"""
    return (bcrypt.check_password_hash(encrypted, password))

@app_views.route("/")
def home():
    return ("<H1>Home</H1>")

@app_views.route("/register")
def register():
    """Handles the /register route, Registers a new user"""
    return (render_template("select_user.html"))

@app_views.route("/register_customer", methods=["GET", "POST"])
def register_customer():
    """Registers a new customer"""
    form = RegisterCustomerForm()
    if form.validate_on_submit():
        hashed = encrypt_password(form.password.data)
        dct = {
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "email": form.email.data,
            "phone_num": form.phone_num.data,
            "password": hashed
        }
        customer = Customer(**dct)
        customer.save()
        flash("Your account has been created!")
        return (redirect(url_for("app_views.login")))
    return (render_template("register_customer.html", form=form))
    
@app_views.route("/register_owner", methods=["GET, POST"])
def register_owner():
    """Registers a new owner/restaurants manager"""
    pass

@app_views.route("/register_driver", methods=["GET", "POST"])
def register_driver():
    """Registers a new driver"""
    pass

@app_views.route("/login", methods=["GET", "POST"])
def login():
    """Handles the /login route, Logs user to the application"""
    form = LoginForm()
    if form.validate_on_submit():
        user = db.filter_by_attr(User, "email", form.email.data)
        if user != [] and check_password(user[0].password,
                                            form.password.data):
            login_user(user[0], remember=form.remember.data)
            return (redirect(url_for("app_views.home")))
        else:
            print("Not registered")
    return (render_template("login.html", form=form))
