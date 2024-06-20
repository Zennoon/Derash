#!/usr/bin/python3
"""
Contains:
    Global
    ======
    api_views - Flask blueprint holding the api routes to be registered
    to the app
"""
from flask import Blueprint, jsonify, request


api_views = Blueprint("api_views", __name__, url_prefix="/api/v1")

@api_views.errorhandler(404)
def not_found():
    """Error handler function for unfound resources"""
    return ({"error": "Not Found"}, 404)

from flask_app.api.v1.views.customers import *