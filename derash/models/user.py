#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    User - Parent class to Customer, Owner, and Driver classes.
    Contains the common attributes that
    all user instances must contains
"""
import random

from flask_login import UserMixin
from sqlalchemy import Column, String
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer

import derash.models
from derash import app, login_manager
from derash.models.base_model import BaseModel


@login_manager.user_loader
def load_user(user_id):
    """Loads a user object given its ID"""
    return (derash.models.db.get(User, user_id))

class User(BaseModel, UserMixin):
    """Parent class for all user classes (Customer, Owner, Driver)"""
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    phone_num = Column(String(10), nullable=False)
    password = Column(String(60), nullable=False)
    image_file = Column(String(20), nullable=False)

    def __init__(self, **kwargs):
        """Initializes a new instance"""
        self.image_file = "default_{}".format(random.randint(0, 9))
        super().__init__(**kwargs)

    def get_reset_token(self):
        """Generates a timed token"""
        s = Serializer(app.config["SECRET_KEY"])
        token = s.dumps({"user_id": self.id})
        return (token)
    
    @staticmethod
    def verify_reset_token(token):
        """Verifies that a token exists and hasn't expired
        (max age is 3600 seconds / 1 Hour)"""
        s = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token, max_age=3600)["user_id"]
        except Exception:
            return (None)
        user = derash.models.db.get(User, user_id)
        return (user)
