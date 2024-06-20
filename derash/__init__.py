from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SECRET_KEY"] = "9bcd272c33a05482e0913cccdb4013bd"
cors = CORS(app, resources={
    r"/api/*": {"origins": "*"}
})
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from derash.routes.api.api_views import *
from derash.routes.app.app_views import *
