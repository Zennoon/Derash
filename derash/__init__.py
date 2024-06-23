import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SECRET_KEY"] = "9bcd272c33a05482e0913cccdb4013bd"
cors = CORS(app, resources={
    r"/api/*": {"origins": "*"}
})
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.config["MAIL_SERVER"] = 'smtp.googlemail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_SERVER"] = 'smtp.googlemail.com'
app.config["MAIL_USERNAME"] = os.getenv("EMAIL_USER")
app.config["MAIL_PASSWORD"] = os.getenv("EMAIL_PWD")
mail = Mail(app)


from derash.routes.app.app_views import *
from derash.routes.api.customer import *
from derash.routes.api.driver import *
from derash.routes.api.owner import *
