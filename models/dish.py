#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    Dish - A concrete class representing a dish from a restaurant
"""
import random

from sqlalchemy import Column, ForeignKey, Float, String, Text

from models import default_pics
from models.base_model import Base, BaseModel


class Dish(BaseModel, Base):
    """A dish that is served by a restaurant"""
    name = Column(String(60), nullable=False)
    description = Column(Text, nullable=True)
    restaurant_id = Column(String(120), ForeignKey("restaurants.id"),
                           nullable=False)
    ingredients = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    image_file = Column(String(20), nullable=False,
                        default=default_pics[random.randint(0, 9)])
