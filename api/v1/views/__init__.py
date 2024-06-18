#!/usr/bin/python3
"""
Contains:
    Global
    ======
    app_views - Flask blueprint holding views, to be registered to the app
"""
from flask import Blueprint


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
