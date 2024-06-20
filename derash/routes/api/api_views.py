#!/usr/bin/python3
"""
Contains Route handler functions for the api
"""
from flask import jsonify, request
from flask_login import current_user

from derash import app
from derash.models import db
from derash.models.restaurant import Restaurant
from utils import calc_distance


@app.route("/api/restaurants")
def get_all_restaurants():
    """Retrieves all restaurants"""
    restaurants = [restaurant.to_dict()
                   for restaurant in db.all(Restaurant)]
    return (jsonify(restaurants))

@app.route("/api/restaurants/nearme", methods=["POST"])
def get_restaurants_near_me():
    """Retrieves restaurants near requesting customer"""
    print(current_user)
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
