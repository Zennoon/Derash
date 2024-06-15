#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    Owner - A concrete class representing a user who manages restaurants
"""
from sqlalchemy.orm import relationship

from models.base_model import Base
from models.user import User


class Owner(User, Base):
    """A user who owns/manages restaurants"""
    __tablename__ = "owners"
    restaurants = relationship("Restaurant", backref="owner")