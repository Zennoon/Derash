#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    Order - A concrete class representing a customer order to restaurant to be
    delivered by a driver
"""
from sqlalchemy import Boolean, Column, ForeignKey, Float, String, Text

from models.base_model import Base, BaseModel


class Order(BaseModel, Base):
    """An order made by a customer"""
    customer_id = Column(String(120), ForeignKey("customers.id"), nullable=False)
    driver_id = Column(String(120), ForeignKey("drivers.id"), nullable=False)
    restaurant_id = Column(String(120), ForeignKey("restaurants.id", nullable=False))
    delivered = Column(Boolean, nullable=False, default=False)
    destination_latitude = Column(Float, nullable=False)
    destination_longitude = Column(Float, nullable=False)
    dishes = Column(Text, nullable=False)
