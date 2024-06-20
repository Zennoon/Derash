#!/usr/bin/python3
"""
Contains Route handler functions for api endpoints concerning customer
"""
from flask import jsonify, redirect, request
from flask_login import current_user, login_required

from derash import app
from derash.models import db
from derash.models.customer import Customer
from derash.models.dish import Dish
from derash.models.order import Order
from derash.models.restaurant import Restaurant
from derash.models.user import User
from utils import calc_distance


@app.route("/api/customer/restaurants")
@login_required
def get_all_restaurants():
    """Retrieves all restaurants"""
    if not isinstance(current_user, Customer):
        return ("Not authorized", 401)
    restaurants = [restaurant.to_dict()
                   for restaurant in db.all(Restaurant)]
    return (jsonify(restaurants))

@app.route("/api/customer/restaurants_nearme", methods=["POST"])
@login_required
def get_restaurants_near_me():
    """Retrieves restaurants near requesting customer"""
    if not isinstance(current_user, Customer):
        return ("Not authorized", 401)
    try:
        data = request.get_json()
    except Exception:
        return ("Expected JSON", 400)
    if data.get("coords") is None:
        return ("Missing coords", 400)
    customer_coords = tuple(data["coords"])
    restaurants = db.all(Restaurant)
    near_me = []
    for restaurant in restaurants:
        restaurant_coords = (restaurant.latitude,
                             restaurant.longitude)
        if calc_distance(customer_coords,
                         restaurant_coords) <= 10:
            near_me.append(restaurant.to_dict())
    return (jsonify(near_me))

@app.route("/api/customer/restaurants/<restaurant_id>")
@login_required
def get_restaurant_details(restaurant_id):
    """Retrieves information about a restaurant"""
    if not isinstance(current_user, Customer):
        return ("Not authorized", 401)
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None:
        return ("Invalid restaurant id", 400)
    dct = restaurant.to_dict()
    dct["dishes"] = [dish.to_dict() for dish in restaurant.dishes]
    return (jsonify(dct))

@app.route("/api/customer/dish/<dish_id>")
@login_required
def get_dish_details(dish_id):
    """Retrieves information about a dish"""
    dish = db.get(Dish, dish_id)
    if dish is None:
        return ("Invalid dish id", 400)
    return (jsonify(dish.to_dict()))

@app.route("/api/customer/pending_orders")
@login_required
def get_pending_orders():
    """Retrieves the pending orders of a customer"""
    if not isinstance(current_user, Customer):
        return ("Not authorized", 401)
    pending = []
    for order in current_user.all_orders:
        if not order.delivered:
            pending.append(order.to_dict())
    return (jsonify(pending))

@app.route("/api/customer/all_orders")
@login_required
def get_all_orders():
    """Retrieves all the past orders of a customer"""
    if not isinstance(current_user, Customer):
        return ("Not authorized", 401)
    orders = [order.to_dict()
              for order in current_user.all_orders]
    return (jsonify(orders))

@app.route("/api/customer/make_order", methods=["POST"])
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
    new_order.driver_id = "0"
    new_order.restaurant_id = data["restaurant_id"]
    for dish_id, amt in data["dishes"].items:
        dish = db.get(Dish, dish_id)
        for i in range(amt):
            new_order.add_dish_to_order(dish)
    new_order.calc_order_price()
    new_order.save()
    return (jsonify(new_order.to_dict()))

@app.route("/api/order/<order_id>")
@login_required
def get_order_details(order_id):
    """Retrieves info about an order"""
    if not isinstance(current_user, User):
        return ("Not authorized", 401)
    order = db.get(Order, order_id)
    if order is None:
        return ("Invalid order id", 400)
    if order not in current_user.all_orders:
        return ("Not authorized", 401)
    all_dishes = [assoc.dish for assoc in order.dishes]
    unique_dishes = {}
    for dish in all_dishes:
        if dish.id in unique_dishes:
            unique_dishes[dish.id] += 1
        else:
            unique_dishes[dish.id] = 1
    dct = order.to_dict()
    dct["dishes"] = unique_dishes
    return (jsonify(dct))