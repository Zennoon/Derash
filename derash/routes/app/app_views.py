#!/usr/bin/python3
"""
Contains Route handler functions for the app
"""
import os
import secrets

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Mail, Message

from derash import app, bcrypt, mail
from derash.forms.dish import createDish, updateDish
from derash.forms.login import LoginForm
from derash.forms.register import RegisterCustomerForm, RegisterDriverForm, RegisterOwnerForm
from derash.forms.reset import RequestResetForm, ResetPasswordForm
from derash.forms.restaurant import createRestaurant, updateRestaurant

from derash.models import db
from derash.models.customer import Customer
from derash.models.dish import Dish
from derash.models.driver import Driver
from derash.models.owner import Owner
from derash.models.restaurant import Restaurant
from derash.models.user import User


def encrypt_password(password):
    """Encrypts user submitted password using bcrypt"""
    return (bcrypt.generate_password_hash(password).decode("utf-8"))

def check_password(encrypted, password):
    """Checks that a user submitted password at login is correct"""
    return (bcrypt.check_password_hash(encrypted, password))

def save_image_file(form_picture, folder):
    """Saves the form submitted image"""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    image_filename = random_hex + f_ext
    save_path = os.path.join(app.root_path, 'static/images/{}'.format(folder), image_filename)
    form_picture.save(save_path)
    return (image_filename)

@app.route("/", methods=["GET", "POST"])
def home():
    if current_user.is_authenticated:
        if isinstance(current_user, Customer):
            return (render_template("customer_home.html"))
        elif isinstance(current_user, Owner):
            form = createRestaurant()
            if form.validate_on_submit():
                restaurant = Restaurant()
                restaurant.name = form.name.data
                restaurant.latitude = form.latitude.data
                restaurant.longitude = form.longitude.data
                restaurant.owner_id = current_user.id
                if form.description.data:
                    restaurant.description = form.description.data
                if form.image_file.data:
                    image_file = save_image_file(form.image_file.data, "restaurant-pics")
                    restaurant.image_file = image_file
                restaurant.save()
            return (render_template("owner_home.html", form=form))
        elif isinstance(current_user, Driver):
            return (render_template("driver_home.html"))
        return (render_template("logged_in_home.html"))
    return (render_template("logged_out_home.html"))

@app.route("/register")
def register():
    """Handles the /register route, Registers a new user"""
    if current_user.is_authenticated:
        return (redirect(url_for("home")))
    return (render_template("select_user.html"))

@app.route("/register_customer", methods=["GET", "POST"])
def register_customer():
    """Registers a new customer"""
    if current_user.is_authenticated:
        return (redirect(url_for("home")))
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
    if current_user.is_authenticated:
        return (redirect(url_for("home")))
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
    if current_user.is_authenticated:
        return (redirect(url_for("home")))
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
    if current_user.is_authenticated:
        return (redirect(url_for("home")))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.filter_by_attr(User, "email", form.email.data)
        if user != [] and check_password(user[0].password,
                                            form.password.data):
            login_user(user[0], remember=form.remember.data)
            return (redirect(url_for("home")))
        else:
            flash("Incorrect credentials. Please check the email and password")
    return (render_template("login.html", form=form))

@app.route("/logout")
@login_required
def logout():
    """Handles the /logout route, logs user out of the application"""
    logout_user()
    return (redirect(url_for("login")))

def send_reset_token(user):
    """Sends instructions on how to reset password to requesting user"""
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
                  sender="noreply@demo.com",
                  recipients=[user.email])
    msg.body = "To reset your password, visit the following link: {}".format(url_for("reset_password", token=token, _external=True))
    msg.send()

@app.route("/reset_password", methods=["GET", "POST"])
def request_reset_password():
    """Handles the /reset_password route, handles requests to reset user password"""
    if current_user.is_authenticated:
        return (redirect(url_for("home")))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = db.filter_by_attr(User, "email", form.email.data)[0]
        send_reset_token(user)
        flash("An email has been sent with instructions on how to reset your password")
        return (redirect(url_for("login")))
    return (render_template("reset_request.html", form=form))

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """Handles the /reset_password/<token> route, resets a user's password if
    token is valid"""
    if current_user.is_authenticated:
        return (redirect(url_for("home")))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token")
        return (redirect(url_for("request_reset_password")))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = bcrypt.generate_password_hash(form.password.data)
        user.save()
    return (render_template("reset_password.html", form=form))

@app.route("/c/restaurants/<restaurant_id>")
@login_required
def view_restaurant_customer(restaurant_id):
    """Displays a restaurant in detail"""
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None:
        return ("Not a valid restaurant id", 404)
    dct  = restaurant.to_dict()
    dct["dishes"] = [dish.to_dict() for dish in restaurant.dishes]
    return (render_template("customer_restaurant.html", restaurant=dct))

@app.route("/o/restaurants/<restaurant_id>", methods=["GET", "POST"])
@login_required
def view_restaurant_owner(restaurant_id):
    """Displays an owner's restaurant in detail"""
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None:
        return ("Not a valid restaurant id", 404)
    dct = restaurant.to_dict()
    dct["dishes"] = [dish.to_dict() for dish in restaurant.dishes]
    return (render_template("owner_restaurant.html"))

@app.route("/o/restaurants/<restaurant_id>/update", methods=["GET", "POST"])
@login_required
def update_restaurant(restaurant_id):
    """Displays an owner's restaurant in detail"""
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None:
        return ("Not a valid restaurant id", 404)
    if restaurant.owner_id != current_user.id:
        return ("Not authorized", 401)
    form = updateRestaurant()
    if form.validate_on_submit():
        restaurant.name = form.name.data
        restaurant.latitude = form.latitude.data
        restaurant.longitude = form.longitude.data
        if form.description.data:
            restaurant.description = form.description.data
        if form.image_file.data:
            image_file = save_image_file(form.image_file.data)
            restaurant.image_file = image_file
        restaurant.save()
        return (redirect(url_for('view_restaurant_owner', restaurant_id=restaurant_id)))
    elif request.method == "GET":
        form.name.data = restaurant.name
        form.description.data = restaurant.description
        form.latitude.data = restaurant.latitude
        form.longitude.data = restaurant.longitude
    return (render_template("update_restaurant.html", restaurant_name=restaurant.name, form=form))

@app.route("/o/restaurants/<restaurant_id>/add-dish", methods=["GET", "POST"])
@login_required
def create_dish(restaurant_id):
    """Page to create a new form"""
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None:
        return ("Not a valid restaurant id", 404)
    dish_form = createDish()
    if dish_form.validate_on_submit():
        dish = Dish()
        dish.restaurant_id = restaurant_id
        dish.name = dish_form.name.data
        dish.ingredients = dish_form.ingredients.data
        dish.price = dish_form.price.data
        if dish_form.description.data:
            dish.description = dish_form.description.data
        if dish_form.image_file.data:
            image_file = save_image_file(dish_form.image_file.data, "dish-pics")
            dish.image_file = image_file
        dish.save()
        return (redirect(url_for('view_restaurant_owner', restaurant_id=restaurant_id)))         
    return (render_template("new_dish.html", restaurant_name=restaurant.name, dish_form=dish_form))
