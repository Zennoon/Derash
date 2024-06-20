#!/usr/bin/python3
"""
Contains:
    Global
    ======
    app - Flask application serving our dynamic content and the API
"""
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SECRET_KEY'] = "e27025c7952742bf0b92c9213aff1014"
cors = CORS(app, resources={
    r"/api/v1/*": {"origins": "*"}
})
login_manager = LoginManager(app)

from flask_app.api.v1.views import api_views
from flask_app.dynamic.views import app_views
app.register_blueprint(api_views)
app.register_blueprint(app_views)

from models import db

@app.teardown_appcontext
def renew_session(ext):
    """Renews the database session"""
    db.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
