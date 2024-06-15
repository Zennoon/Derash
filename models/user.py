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

from sqlalchemy import Column, String

from models.base_model import BaseModel


class User(BaseModel):
    """Parent class for all user classes (Customer, Owner, Driver)"""
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    phone_num = Column(String(10), nullable=False)
    password = Column(String(20), nullable=False)
    image_file = Column(String(20), nullable=False,
                        default="default_{}".format(random.randint(0, 9)))
