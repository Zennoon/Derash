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

from flask_app.app import login_manager
import models
from models.base_model import BaseModel


@login_manager.user_loader
def load_user(user_id):
    """Loads a user object given its ID"""
    return (models.db.get(User, user_id))

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
