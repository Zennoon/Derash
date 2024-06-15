#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    Review - A concrete class representing a restaurant review made by a customer
"""
from sqlalchemy import Column, ForeignKey, String, Text

from models.base_model import Base, BaseModel


class Review(BaseModel, Base):
    """A restaurant review made by a customer"""
    customer_id = Column(String(120), ForeignKey("customers.id"), nullable=False)
    restaurant_id = Column(String(120), ForeignKey("restaurants.id"), nullable=False)
    text = Column(Text, nullable=False)
