#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    Dish - A concrete class representing a dish from a restaurant
"""
import random

from sqlalchemy import Column, ForeignKey, Float, String, Text

from derash.models.base_model import Base, BaseModel


class Dish(BaseModel, Base):
    """A dish that is served by a restaurant"""
    __tablename__ = "dishes"
    name = Column(String(60), nullable=False)
    description = Column(Text, nullable=True)
    restaurant_id = Column(String(120), ForeignKey("restaurants.id"),
                           nullable=False)
    ingredients = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    image_file = Column(String(20), nullable=False)

    def __init__(self, **kwargs):
        """Initializes a new instance"""
        self.image_file = "default_{}".format(random.randint(0, 9))
        super().__init__(**kwargs)
