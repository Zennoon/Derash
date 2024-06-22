#!/usr/bin/python3
"""
Contains Route handler functions for api endpoints concerning customer
"""
from flask import jsonify, redirect, request, url_for
from flask_login import current_user, login_required

from derash import app
from derash.models import db
from derash.models.base_model import BaseModel
from derash.models.customer import Customer
from derash.models.driver import Driver
from derash.models.dish import Dish
from derash.models.order import Order
from derash.models.restaurant import Restaurant
from derash.models.user import User
from utils import calc_distance


default_driver = db.get(Driver, "0")


@app.route("/api/customer")
def get_customer_details():
    """Returns info about customer"""
    if not isinstance(current_user, Customer):
        return ("Not authorized", 401)
    return (jsonify(current_user.to_dict()))

@app.route("/api/customer/all_restaurants")
@login_required
def get_all_restaurants():
    """Retrieves all restaurants"""
    if not isinstance(current_user, Customer):
        return ("Not authorized", 401)
    restaurants = [restaurant.to_dict()
                   for restaurant in db.all(Restaurant)]
    return (jsonify(restaurants))


@app.route("/api/customer/open_restaurants")
@login_required
def get_open_restaurants():
    """Retrieves all open restaurants"""
    if not isinstance(current_user, Customer):
        return ("Not authorized", 401)
    restaurants = [restaurant.to_dict()
                   for restaurant in db.all(Restaurant)
                   if restaurant.is_open]
    return (jsonify(restaurants))

@app.route("/api/customer/restaurants_near", methods=["POST"])
@login_required
def get_restaurants_near():
    """Retrieves restaurants near given coords"""
    if not isinstance(current_user, Customer):
        return ("Not authorized", 401)
    try:
        data = request.get_json()
    except Exception:
        return ("Expected JSON", 400)
    if data.get("coords") is None:
        return ("Missing coords", 400)
    customer_coords = tuple(data["coords"])
    restaurants = [restaurant
                   for restaurant in db.all(Restaurant)
                   if restaurant.is_open]
    near_me = []
    for restaurant in restaurants:
        restaurant_coords = (restaurant.latitude,
                             restaurant.longitude)
        if calc_distance(customer_coords,
                         restaurant_coords) <= 20:
            near_me.append(restaurant.to_dict())
    return (jsonify(near_me))

@app.route("/api/customer/restaurants/<restaurant_id>")
@login_required
def get_restaurant_details(restaurant_id):
    """Retrieves information about a restaurant"""
    if not isinstance(current_user, Customer):
        return ("Not authorized", 401)
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None or not restaurant.is_open:
        return ("Invalid restaurant id", 400)
    dct = restaurant.to_dict()
    dct["dishes"] = [dish.to_dict() for dish in restaurant.dishes]
    return (jsonify(dct))

@app.route("/api/customer/restaurants/<restaurant_id>/reviews")
@login_required
def get_restaurant_reviews(restaurant_id):
    """Retrieves the reviews of a restaurant"""
    if not isinstance(current_user, Customer):
        return ("Not authorized", 401)
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None:
        return ("Invalid restaurant id", 400)
    reviews = [review.to_dict() for review in restaurant.reviews]
    return (jsonify(reviews))

@app.route("/api/customer/dishes/<dish_id>")
@login_required
def get_dish_details(dish_id):
    """Retrieves information about a dish"""
    dish = db.get(Dish, dish_id)
    if dish is None:
        return ("Invalid dish id", 400)
    return (jsonify(dish.to_dict()))

@app.route("/api/customer/past_orders")
@login_required
def get_past_orders():
    """Retrieves the past (completed) orders of a customer"""
    if not isinstance(current_user, Customer):
        return ("Not authorized", 401)
    past_orders = []
    for order in current_user.all_orders:
        if order.customer_confirm and order.driver_confirm:
            dct = order.to_dict()
            dct["dishes"] = {}
            all_dishes = [assoc.dish for assoc in order.dishes]
            for dish in all_dishes:
                if dish.id in dct["dishes"]:
                    dct["dishes"][dish.id] += 1
                else:
                    dct["dishes"][dish.id] = 1
            past_orders.append(dct)
    return (jsonify(past_orders))

@app.route("/api/customer/pending_orders")
@login_required
def get_pending_orders():
    """Retrieves the pending orders of a customer"""
    if not isinstance(current_user, Customer):
        return ("Not authorized", 401)
    pending_orders = []
    for order in current_user.all_orders:
        if (not order.customer_confirm) or (not order.driver_confirm):
            dct = order.to_dict()
            dct["dishes"] = {}
            all_dishes = [assoc.dish for assoc in order.dishes]
            for dish in all_dishes:
                if dish.id in dct["dishes"]:
                    dct["dishes"][dish.id] += 1
                else:
                    dct["dishes"][dish.id] = 1
            pending_orders.append(dct)
    return (jsonify(pending_orders))

@app.route("/api/customer/all_orders")
@login_required
def get_all_orders():
    """Retrieves all the past orders of a customer"""
    if not isinstance(current_user, Customer):
        return ("Not authorized", 401)
    all_orders = []
    for order in current_user.all_orders:
        dct = order.to_dict()
        dct["dishes"] = {}
        all_dishes = [assoc.dish for assoc in order.dishes]
        for dish in all_dishes:
            if dish.id in dct["dishes"]:
                dct["dishes"][dish.id] += 1
            else:
                dct["dishes"][dish.id] = 1
        all_orders.append(dct)
    return (jsonify(all_orders))

@app.route("/api/customer/confirm_delivered/<order_id>", methods=["PUT"])
@login_required
def confirm_order_delivered(order_id):
    """Confirms that order has been delivered to customer"""
    if not isinstance(current_user, Customer):
        return ("Not authorized", 401)
    order = db.get(Order, order_id)
    if order is None:
        return ("Invalid order id", 400)
    if order not in current_user.all_orders:
        return ("Not authorized", 401)
    order.customer_confirm = True
    order.save()
    return (jsonify(True))

@app.route("/api/customer/orders/<order_id>")
@login_required
def get_order_details(order_id):
    """Retrieves info about an order"""
    if not isinstance(current_user, Customer):
        return ("Not authorized", 401)
    order = db.get(Order, order_id)
    if order is None:
        return ("Invalid order id", 400)
    if order not in current_user.all_orders:
        return ("Not authorized", 401)
    all_dishes = [assoc.dish for assoc in order.dishes]
    unique_dishes = {}
    for dish in all_dishes:
        print(dish.price)
        if dish.id in unique_dishes:
            unique_dishes[dish.id] += 1
        else:
            unique_dishes[dish.id] = 1
    dct = order.to_dict()
    dct["dishes"] = unique_dishes
    return (jsonify(dct))

@app.route("/api/customer/new_order", methods=["POST"])
@login_required
def create_order():
    """Creates a new order"""
    if not isinstance(current_user, Customer):
        return ("Not authorized", 401)
    try:
        data = request.get_json()
    except Exception:
        return ("Expected JSON", 400)
    for attr in ["destination_latitude", "destination_longitude",
                 "restaurant_id", "dishes"]:
        if attr not in data:
            return ("Incomplete data. Can't create order", 400)
    new_order = Order()
    new_order.destination_latitude = data["destination_latitude"]
    new_order.destination_longitude = data["destination_longitude"]
    new_order.customer_id = current_user.id
    new_order.driver_id = default_driver.id
    new_order.restaurant_id = data["restaurant_id"]
    for dish_id, amt in data["dishes"].items():
        dish = db.get(Dish, dish_id)
        for i in range(amt):
            new_order.add_dish_to_order(dish)
    new_order.calc_order_price()
    print(new_order.id)
    return (jsonify(True))
