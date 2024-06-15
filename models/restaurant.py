#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    Restaurant - A concrete class representing a restaurant that accepts orders
"""
import random

from sqlalchemy import Column, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from models import default_pics
from models.base_model import Base, BaseModel


class Restaurant(BaseModel, Base):
    """A restaurant that accepts orders from customers"""
    __tablename__ = "restaurants"
    name = Column(String(60), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(String(120), ForeignKey("owners.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    image_file = Column(String(20), nullable=False, default=default_pics[random.randint(0, 9)])
    all_orders = relationship("Order", backref="restaurant")
    dishes = relationship("Dish", backref="restaurant",
                          cascade="all, delete, delete-orphan")
    reviews = relationship("Review", backref="restaurant",
                           cascade="all, delete, delete-orphan")
    
    def get_pending_orders(self):
        """Returns the pending orders of the restaurant"""
        return (list(filter(lambda order: order.delivered == False, self.all_orders)))
