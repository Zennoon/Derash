#!/usr/bin/python3
"""
Contains:
    Global
    ======
    app_views - Blueprint holding routes for the
    application
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__)

from flask_app.dynamic.views.routes import *