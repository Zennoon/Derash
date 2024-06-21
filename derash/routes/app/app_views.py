#!/usr/bin/python3
"""
Contains Route handler functions for the app
"""
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from derash import app, bcrypt
from derash.forms.register import RegisterCustomerForm, RegisterDriverForm, RegisterOwnerForm
from derash.forms.login import LoginForm

from derash.models import db
from derash.models.customer import Customer
from derash.models.driver import Driver
from derash.models.owner import Owner
from derash.models.user import User


def encrypt_password(password):
    """Encrypts user submitted password using bcrypt"""
    return (bcrypt.generate_password_hash(password).decode("utf-8"))

def check_password(encrypted, password):
    """Checks that a user submitted password at login is correct"""
    return (bcrypt.check_password_hash(encrypted, password))

@app.route("/")
def home():
    return (render_template("testing.html"))

@app.route("/register")
def register():
    """Handles the /register route, Registers a new user"""
    return (render_template("select_user.html"))

@app.route("/register_customer", methods=["GET", "POST"])
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
        return (redirect(url_for("login")))
    return (render_template("register_customer.html", form=form))
    
@app.route("/register_owner", methods=["GET", "POST"])
def register_owner():
    """Registers a new owner/restaurants manager"""
    form = RegisterOwnerForm()
    if form.validate_on_submit():
        hashed = encrypt_password(form.password.data)
        dct = {
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "email": form.email.data,
            "phone_num": form.phone_num.data,
            "password": hashed
        }
        owner = Owner(**dct)
        owner.save()
        flash("Your account has been created!")
        return (redirect(url_for("login")))
    return (render_template("register_owner.html", form=form))

@app.route("/register_driver", methods=["GET", "POST"])
def register_driver():
    """Registers a new driver"""
    form = RegisterDriverForm()
    if form.validate_on_submit():
        hashed = encrypt_password(form.password.data)
        dct = {
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "email": form.email.data,
            "phone_num": form.phone_num.data,
            "password": hashed,
            "license_num": form.license_num.data
        }
        driver = Driver(**dct)
        driver.save()
        flash("Your account has been created!")
        return (redirect(url_for("login")))
    return (render_template("register_driver.html", form=form))

@app.route("/login", methods=["GET", "POST"])
def login():
    """Handles the /login route, Logs user to the application"""
    form = LoginForm()
    if form.validate_on_submit():
        user = db.filter_by_attr(User, "email", form.email.data)
        if user != [] and check_password(user[0].password,
                                            form.password.data):
            login_user(user[0], remember=form.remember.data)
            return (redirect(url_for("home")))
        else:
            print("Not registered")
    return (render_template("login.html", form=form))

@app.route("/logout")
def logout():
    """Handles the /logout route, logs user out of the application"""
    logout_user()
    return (redirect(url_for("login")))
