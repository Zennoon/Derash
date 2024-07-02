#!/usr/bin/python3
"""
Contains Route handler functions for the app
"""
import os
import secrets

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message
from PIL import Image

from derash import app, bcrypt, mail
from derash.forms.dish import createDish, updateDish
from derash.forms.login import LoginForm
from derash.forms.register import RegisterCustomerForm, RegisterDriverForm, RegisterOwnerForm
from derash.forms.reset import RequestResetForm, ResetPasswordForm
from derash.forms.restaurant import createRestaurant, updateRestaurant
from derash.forms.user_update import UpdateAccountForm, UpdateDriverAccountForm

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
    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(save_path)
    return (image_filename)

@app.route("/", methods=["GET", "POST"])
def home():
    if current_user.is_authenticated:
        if isinstance(current_user, Customer):
            return (render_template("customer_home.html", user=current_user.to_dict()))
        elif isinstance(current_user, Owner):
            return (render_template("owner_home.html", user=current_user.to_dict()))
        elif isinstance(current_user, Driver):
            return (render_template("driver_home.html", user=current_user.to_dict()))
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
        flash("Your account has been created!", "success")
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
        flash("Your account has been created!", "success")
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
        flash("Your account has been created!", "success")
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
            flash("Incorrect credentials. Please check the email and password", "error")
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
        flash("An email has been sent with instructions on how to reset your password", "info")
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
        flash("That is an invalid or expired token", "warning")
        return (redirect(url_for("request_reset_password")))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = bcrypt.generate_password_hash(form.password.data)
        user.save()
    return (render_template("reset_password.html", form=form))

@app.route("/o/new-restaurant", methods=["GET", "POST"])
@login_required
def add_new_restaurant():
    """Handles creating a new restaurant"""
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
    return (render_template("new_restaurant.html", form=form))

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
    return (render_template("owner_restaurant.html", restaurant=dct, user=current_user.to_dict()))

@app.route("/o/restaurants/<restaurant_id>/update", methods=["GET", "POST"])
@login_required
def update_restaurant(restaurant_id):
    """Modifies an existing restaurant"""
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
            image_file = save_image_file(form.image_file.data, "restaurant-pics")
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
    """Handles creating a new dish"""
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None:
        return ("Not a valid restaurant id", 404)
    if restaurant.owner_id != current_user.id:
        return ("Not authorized", 401)
    form = createDish()
    if form.validate_on_submit():
        dish = Dish()
        dish.restaurant_id = restaurant_id
        dish.name = form.name.data
        dish.ingredients = form.ingredients.data
        dish.price = form.price.data
        if form.description.data:
            dish.description = form.description.data
        if form.image_file.data:
            image_file = save_image_file(form.image_file.data, "dish-pics")
            dish.image_file = image_file
        dish.save()
        return (redirect(url_for('view_restaurant_owner', restaurant_id=restaurant_id)))         
    return (render_template("new_dish.html", restaurant_name=restaurant.name, form=form))

@app.route("/o/dish/<dish_id>/edit", methods=["GET", "POST"])
@login_required
def update_dish(dish_id):
    """Modifies an existing dish"""
    dish = db.get(Dish, dish_id)
    if dish is None:
        return ("Not a valid dish id", 404)
    restaurant = db.get(Restaurant, dish.restaurant_id)
    if restaurant.owner_id != current_user.id:
        return ("Not authorized", 401)
    form = updateDish()
    if form.validate_on_submit():
        dish.name = form.name.data
        dish.ingredients = form.ingredients.data
        dish.price = form.price.data
        if form.description.data:
            dish.description = form.description.data
        if form.image_file.data:
            image_file = save_image_file(form.image_file.data, "dish-pics")
            dish.image_file = image_file
        dish.save()
        return (redirect(url_for('view_restaurant_owner', restaurant_id=restaurant.id)))
    elif request.method == "GET":
        form.name.data = dish.name
        form.description.data = dish.description
        form.ingredients.data = dish.ingredients
        form.price.data = dish.price
    return (render_template("update_dish.html", dish_name=dish.name, form=form))

@app.route("/account", methods=["GET", "POST"])
@login_required
def view_profile():
    if isinstance(current_user, Customer) or isinstance(current_user, Owner):
        form = UpdateAccountForm()
    elif isinstance(current_user, Driver):
        form = UpdateDriverAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone_num = form.phone_num.data
        if form.image_file.data:
            image_file = save_image_file(form.image_file.data, "profile-pics")
            current_user.image_file = image_file
        if hasattr(form, "license_num"):
            current_user.license_num = form.license_num.data
        current_user.save()
    elif request.method == "GET":
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.phone_num.data = current_user.phone_num
        if hasattr(form, "license_num"):
            form.license_num.data = current_user.license_num
    return (render_template("account.html", form=form, user=current_user))
    