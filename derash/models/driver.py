#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    Driver - A concrete class representing a user who delivers orders
"""
from sqlalchemy import Boolean, Column, Float, String
from sqlalchemy.orm import relationship

from derash.models.base_model import Base
from derash.models.order import Order
from derash.models.user import User


class Driver(User, Base):
    """A user who delivers orders to customers"""
    __tablename__ = "drivers"
    license_num = Column(String(20), nullable=False)
    active = Column(Boolean, nullable=False, default=False)
    delivering = Column(Boolean, nullable=False, default=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    all_orders = relationship("Order", backref="driver")
