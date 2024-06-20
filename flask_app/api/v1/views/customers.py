#!/usr/bin/python3
"""
Contains:
    Functions
    =========
    route handler functions for api requests concerning customers, and related
    models
"""
from flask import jsonify, request

from flask_app.api.v1.views import api_views
import models
from models.customer import Customer
from models.restaurant import Restaurant
from utils import calc_distance


@api_views.route("/customer/all_restaurants", methods=["GET"])
def get_all_restaurants():
    """
    Returns all restaurants registered
    """
    restaurants = [restaurant.to_dict() for restaurant in models.db.all(Restaurant)]
    return (jsonify(restaurants))

@api_views.route("/customer/restaurants_nearme", methods=["POST"])
def get_restaurants_nearme():
    """
    Returns restaurants near the requesting customer
    
    Request body is expected to contain coordinates of the customer
    """
    try:
        data = request.get_json()
    except Exception:
        return ("Not JSON", 400)
    if "coords" not in data:
        return ("Missing customer coords", 400)
    customer_coords = tuple(data.get("coords"))
    restaurants = models.db.all(Restaurant)
    near_me = []
    for restaurant in restaurants:
        restaurant_coords = (restaurant.latitude,
                             restaurant.longitude)
        if calc_distance(customer_coords, restaurant_coords) < 15:
            near_me.append(restaurant.to_dict())
    return (jsonify(near_me))

@api_views.route("/customer/history")
def get_customer_history():
    """Retrieves the customer's past orders"""
        
@api_views.route("/customer/pending_orders")
def get_customer_pending_orders():
    """Retrieves the customer's pending (not delivered) orders"""
    

