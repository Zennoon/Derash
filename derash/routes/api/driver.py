#!/usr/bin/python3
"""
Contains Route handler functions for api endpoints concerning drivers
"""
from datetime import datetime

from flask import jsonify, request
from flask_login import current_user, login_required

from derash import app
from derash.models import db
from derash.models.driver import Driver
from derash.models.order import Order
from derash.models.restaurant import Restaurant
from utils import calc_distance


default_driver = db.get(Driver, "0")

@app.route("/api/driver")
@login_required
def get_driver_details():
    """Returns info about driver"""
    if not isinstance(current_user, Driver):
        return ("Not authorized", 401)
    return (jsonify(current_user.to_dict()))

@app.route("/api/driver/all_deliveries")
@login_required
def get_all_deliveries():
    """Retrieves all of a driver's deliveries"""
    if not isinstance(current_user, Driver):
        return ("Not authorized", 401)
    
    all_deliveries = []
    for delivery in current_user.all_orders:
        dct = delivery.to_dict()
        dct["dishes"] = {}
        all_dishes = [assoc.dish for assoc in delivery.dishes]
        for dish in all_dishes:
            if dish.id in dct["dishes"]:
                dct["dishes"][dish.id] += 1
            else:
                dct["dishes"][dish.id] = 1
        all_deliveries.append(dct)
    return (jsonify(all_deliveries))

@app.route("/api/driver/past_deliveries")
@login_required
def get_past_deliveries():
    """Retrieves all completed orders/deliveries"""
    if not isinstance(current_user, Driver):
        return ("Not authorized", 401)
    past_deliveries = []
    for delivery in current_user.all_orders:
        if delivery.customer_confirm and delivery.driver_confirm:
            dct = delivery.to_dict()
            dct["dishes"] = {}
            all_dishes = [assoc.dish for assoc in delivery.dishes]
            for dish in all_dishes:
                if dish.id in dct["dishes"]:
                    dct["dishes"][dish.id] += 1
                else:
                    dct["dishes"][dish.id] = 1
            dct["restaurant"] = delivery.restaurant.to_dict()
            dct["customer"] = delivery.customer.to_dict()
            past_deliveries.append(dct)
    return (jsonify(past_deliveries))

@app.route("/api/driver/possible_deliveries", methods=["POST"])
@login_required
def get_possible_deliveries():
    """Retrieves possible deliveries
    (5 km distance between driver and restaurant)"""
    if not isinstance(current_user, Driver):
        return ("Not authorized", 401)
    try:
        data = request.get_json()
        driver_coords = tuple(data["coords"])
    except Exception:
        return ("Missing driver coordinates", 400)
    possible_deliveries = []
    if current_user.active and not current_user.delivering:
        orders = db.filter_by_attr(Order, "driver_id", default_driver.id)
        for order in orders:
            restaurant = db.get(Restaurant, order.restaurant_id)
            restaurant_coords = (restaurant.latitude,
                                 restaurant.longitude)
            distance = calc_distance(restaurant_coords,
                                     driver_coords)
            print(distance)
            if distance <= 5:
                dct = order.to_dict()
                dct["restaurant"] = restaurant.to_dict()
                dct["customer"] = order.customer.to_dict()
                possible_deliveries.append(dct)
    return (jsonify(possible_deliveries))

@app.route("/api/driver/activate", methods=["PUT"])
@login_required
def activate_driver():
    """Activates driver (open to accept deliveries)"""
    if not isinstance(current_user, Driver):
        return ("Not authorized", 401)
    current_user.active = True
    current_user.save()
    return (jsonify(True))

@app.route("/api/driver/deactivate", methods=["PUT"])
@login_required
def deactivate_driver():
    """Deactivates driver (not open to accept deliveries)"""
    if not isinstance(current_user, Driver):
        return ("Not authorized", 401)
    current_user.active = False
    current_user.save()
    return (jsonify(True))

@app.route("/api/driver/<order_id>/accept", methods=["PUT"])
@login_required
def accept_delivery(order_id):
    """Accepts an order (to be deliveredby current user)"""
    if not isinstance(current_user, Driver):
        return ("Not authorized", 401)
    if not current_user.active:
        return ("You are not active", 400)
    if current_user.delivering:
        return ("You have an unfinished delivery", 400)
    order = db.get(Order, order_id)
    if order is None:
        return ("Invalid order id", 400)
    order.driver_id = current_user.id
    order.save()
    current_user.delivering = True
    current_user.save()
    return (jsonify(True))

@app.route("/api/driver/current_delivery")
@login_required
def get_current_delivery():
    """Retrieves the current order being delivered by current user"""
    if not isinstance(current_user, Driver):
        return ("Not authorized", 401)
    pending_orders = []
    for order in current_user.all_orders:
        if (not order.customer_confirm
        or not order.driver_confirm):
            dishes = [assoc.dish for assoc in order.dishes]
            dct = order.to_dict()
            unique_dishes = {}
            for dish in dishes:
                if dish.id in unique_dishes:
                    unique_dishes[dish.id] += 1
                else:
                    unique_dishes[dish.id] = 1
            dct["dishes"] = unique_dishes
            dct["customer"] = order.customer.to_dict()
            dct["restaurant"] = order.restaurant.to_dict()
            pending_orders.append(dct)
    return (jsonify(pending_orders))

@app.route("/api/driver/<order_id>/delivered", methods=["PUT"])
@login_required
def confirm_delivery_done(order_id):
    """Implements a driver confirming an order's delivery"""
    if not isinstance(current_user, Driver):
        return ("Not authorized", 401)
    order = db.get(Order, order_id)
    if order is None:
        return ("Invalid order id", 400)
    if db.get(Driver, order.driver_id).id != current_user.id:
        return ("Not authorized", 401)
    order.driver_confirm = True
    order.save()
    current_user.delivering = False
    current_user.save()
    return (jsonify(True))

@app.route("/api/driver/monthly")
@login_required
def get_driver_monthly_receipt():
    """Retrieves the deliveries made by a driver in current month"""
    if not isinstance(current_user, Driver):
        return ("Not authorized", 401)
    now = datetime.now()
    created_at = current_user.created_at
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
    deliveries_this_month = []
    for order in current_user.all_orders:
        if (order.customer_confirm
            and order.driver_confirm 
            and order.created_at > base_date):
            deliveries_this_month.append(order.to_dict())
    return (jsonify(deliveries_this_month))

@app.route("/api/driver/past_month")
@login_required
def get_driver_past_month_receipt():
    """Retrieves the deliveries made by a driver in the past month"""
    if not isinstance(current_user, Driver):
        return ("Not authorized", 401)
    now = datetime.now()
    created_at = current_user.created_at
    if now.day >= created_at.day:
        start_month = now.month - 1
        end_month = now.month
    else:
        start_month = now.month - 2
        end_month = now.month - 1
    if start_month < created_at.month:
        return (jsonify(None), 400)

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
    deliveries_past_month = []
    for order in current_user.all_orders:
        if (order.customer_confirm
            and order.driver_confirm
            and order.created_at > start
            and order.created_at < end):
            dct = order.to_dict()
            dct["dishes"] = {}
            dct["dish_names"] = {}
            all_dishes = [assoc.dish for assoc in order.dishes]
            for dish in all_dishes:
                if dish.id in dct["dishes"]:
                    dct["dishes"][dish.id] += 1
                    dct["dish_names"][dish.name] += 1
                else:
                    dct["dishes"][dish.id] = 1
                    dct["dish_names"][dish.name] = 1
            dct["customer"] = order.customer.to_dict()
            dct["restaurant"] = order.restaurant.to_dict()
            deliveries_past_month.append(dct)
    return (jsonify(deliveries_past_month))
