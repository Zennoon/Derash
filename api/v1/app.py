#!/usr/bin/python3
"""
Contains:
    Global
    ======
    app - Flask application to serve the API

    Functions
    =========
    renew_session - Renews the sqlalchemy session after each request

    not_found - Error handler for error code 404 (resource not found)
"""
from flask import Flask, jsonify
from flask_cors import CORS

from api.v1.views import app_views
from models import db

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
cors = CORS(app, resources={
    r"/api/v1/*": {"origins": "*"}
})


@app.teardown_appcontext
def renew_session(self):
    """Renews the SQLAlchemy session"""
    db.close()

@app.errorhandler(404)
def not_found(self):
    """Handles 404 errors"""
    return (jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)