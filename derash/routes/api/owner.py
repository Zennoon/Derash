#!/usr/bin/python3
"""
Contains Route handler functions for api endpoints concerning restaurant managers
"""
from datetime import datetime

from flask import jsonify, request
from flask_login import current_user, login_required

from derash import app
from derash.models import db
from derash.models.dish import Dish
from derash.models.restaurant import Restaurant
from derash.models.review import Review
from derash.models.order import Order
from derash.models.owner import Owner


@app.route("/api/owner")
def get_owner_details():
    """Returns info about owner/manager"""
    if not isinstance(current_user, Owner):
        return ("Not authorized", 401)
    return (jsonify(current_user.to_dict()))

@app.route("/api/owner/my_restaurants")
@login_required
def get_my_restaurants():
    """Retrieves an owners registered restaurants"""
    if not isinstance(current_user, Owner):
        return ("Not authorized", 401)
    restaurants = [restaurant.to_dict() for restaurant in current_user.restaurants]
    return (jsonify(restaurants))

@app.route("/api/owner/my_restaurants/<restaurant_id>")
@login_required
def get_my_restaurant_details(restaurant_id):
    """Retrieves info about an owner's restaurants"""
    if not isinstance(current_user, Owner):
        return ("Not authorized", 401)
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None:
        return ("Invalid restaurant id", 400)
    if restaurant.owner_id != current_user.id:
        return ("Not authorized", 401)
    dct = restaurant.to_dict()
    dct["dishes"] = [dish.to_dict() for dish in restaurant.dishes]
    return (jsonify(dct))

@app.route("/api/owner/my_restaurants/<restaurant_id>/reviews")
@login_required
def get_my_restaurant_reviews(restaurant_id):
    """Retrieves reviews of an owner's restaurants"""
    if not isinstance(current_user, Owner):
        return ("Not authorized", 401)
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None:
        return ("Invalid restaurant id", 400)
    if restaurant.owner_id != current_user.id:
        return ("Not authorized", 401)
    reviews = [review.to_dict() for review in restaurant.reviews]
    return (jsonify(reviews))

@app.route("/api/owner/my_restaurants/<restaurant_id>/open", methods=["PUT"])
@login_required
def open_my_restaurant(restaurant_id):
    """Opens an owner's restaurant"""
    if not isinstance(current_user, Owner):
        return ("Not authorized", 401)
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None:
        return ("Invalid restaurant id", 400)
    if restaurant.owner_id != current_user.id:
        return ("Not authorized", 401)
    restaurant.is_open = True
    restaurant.save()
    return (jsonify(True))

@app.route("/api/owner/my_restaurants/<restaurant_id>/close", methods=["PUT"])
@login_required
def close_my_restaurant(restaurant_id):
    """Closes an owner's restaurant"""
    if not isinstance(current_user, Owner):
        return ("Not authorized", 401)
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None:
        return ("Invalid restaurant id", 400)
    if restaurant.owner_id != current_user.id:
        return ("Not authorized", 401)
    restaurant.is_open = False
    restaurant.save()
    return (jsonify(True))


@app.route("/api/owner/my_restaurants/<restaurant_id>/monthly")
@login_required
def get_restaurant_monthly_receipt(restaurant_id):
    """Retrieves the orders of the current month until now"""
    if not isinstance(current_user, Owner):
        return ("Not authorized", 401)
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None:
        return ("Invalid restaurant id", 400)
    if restaurant.owner_id != current_user.id:
        return ("Not authorized", 401)
    now = datetime.now()
    created_at = restaurant.created_at
    if now.day >= created_at.day:
        base_month = now.month
    else:
        base_month = now.month - 1
    base_date = datetime(year=created_at.year,
                         month=base_month,
                         day=created_at.day, 
                         hour=created_at.hour,
                         minute=created_at.minute,
                         second=created_at.second,
                         microsecond=created_at.microsecond)
    orders_this_month = []
    for order in restaurant.all_orders:
        if (order.restaurant_confirm
        and order.created_at > base_date):
            orders_this_month.append(order.to_dict())
    return (jsonify(orders_this_month))

@app.route("/api/owner/my_restaurants/<restaurant_id>/past_month")
@login_required
def get_restaurant_past_month_receipt(restaurant_id):
    """Retrieves the completed orders of the past month"""
    if not isinstance(current_user, Owner):
        return ("Not authorized", 401)
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None:
        return ("Invalid restaurant id", 400)
    if restaurant.owner_id != current_user.id:
        return ("Not authorized", 401)
    now = datetime.now()
    created_at = restaurant.created_at
    if now.day >= created_at.day:
        start_month = now.month - 1
        end_month = now.month
    else:
        start_month = now.month - 2
        end_month = now.month - 1
    if start_month < created_at.month:
        return ("Restaurant doesn't have enough data", 400)

    start = datetime(year=created_at.year,
                     month=start_month,
                     day=created_at.day,
                     hour=created_at.hour,
                     minute=created_at.minute,
                     second=created_at.second,
                     microsecond=created_at.microsecond)
    end = datetime(year=created_at.year,
                   month=end_month,
                   day=created_at.day,
                   hour=created_at.hour,
                   minute=created_at.minute,
                   second=created_at.second,
                   microsecond=created_at.microsecond)
    orders_past_month = []
    for order in restaurant.all_orders:
        if (order.restaurant_confirm
            and order.created_at > start
            and order.created_at < end):
            orders_past_month.append(order.to_dict())
    return (jsonify(orders_past_month))

@app.route("/api/owner/my_restaurants/<restaurant_id>/all_orders")
@login_required
def get_my_restaurant_all_orders(restaurant_id):
    """Retrieves all the orders of an owner's restaurant"""
    if not isinstance(current_user, Owner):
        return ("Not authorized", 401)
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None:
        return ("Invalid restaurant id", 400)
    if restaurant.owner_id != current_user.id:
        return ("Not authorized", 401)
    all_orders = []
    for order in restaurant.all_orders:
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

@app.route("/api/owner/my_restaurants/<restaurant_id>/past_orders")
@login_required
def get_my_restaurant_past_orders(restaurant_id):
    """Retrieves all the past (done) orders of an owner's restaurant"""
    if not isinstance(current_user, Owner):
        return ("Not authorized", 401)
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None:
        return ("Invalid restaurant id", 400)
    if restaurant.owner_id != current_user.id:
        return ("Not authorized", 401)
    past_orders = []
    for order in restaurant.all_orders:
        if order.restaurant_confirm:
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

@app.route("/api/owner/my_restaurants/<restaurant_id>/pending_orders")
@login_required
def get_my_restaurant_pending_orders(restaurant_id):
    """Retrieves all the past (done) orders of an owner's restaurant"""
    if not isinstance(current_user, Owner):
        return ("Not authorized", 401)
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None:
        return ("Invalid restaurant id", 400)
    if restaurant.owner_id != current_user.id:
        return ("Not authorized", 401)
    pending_orders = []
    for order in restaurant.all_orders:
        if not order.restaurant_confirm:
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

@app.route("/api/owner/my_orders/<order_id>")
@login_required
def get_my_order_details(order_id):
    """Retrieves details about an order"""
    if not isinstance(current_user, Owner):
        return ("Not authorized", 401)
    order = db.get(Order, order_id)
    if order is None:
        return ("Invalid order id", 400)
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

@app.route("/api/owner/my_orders/<order_id>/done", methods=["PUT"])
@login_required
def confirm_order_done(order_id):
    """Confirms that the order has been prepared"""
    if not isinstance(current_user, Owner):
        return ("Not authorized", 401)
    order = db.get(Order, order_id)
    if order is None:
        return ("Invalid order id", 400)
    if order.restaurant not in current_user.restaurants:
        return ("Not authorized", 401)
    order.restaurant_confirm = True
    order.save()
    return (jsonify(True))
