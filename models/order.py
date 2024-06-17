#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    Order - A concrete class representing a customer order to restaurant to be
    delivered by a driver
"""
from uuid import uuid4

from sqlalchemy import Boolean, Column, ForeignKey, Float, String, Table, Text
from sqlalchemy.orm import relationship

import models
from models.base_model import Base, BaseModel
from models.dish import Dish


class Association(BaseModel, Base):
    """Association table between orders and dishes (many to many)"""
    __tablename__ = "association_table"
    order_id = Column(String(120), ForeignKey("orders.id"))
    dish_id = Column(String(120), ForeignKey("dishes.id"))
    extra_data = Column(String(10), nullable=True)
    dish = relationship("Dish", backref="orders")


class Order(BaseModel, Base):
    """An order made by a customer"""
    __tablename__ = "orders"
    customer_id = Column(String(120), ForeignKey("customers.id"),
                         nullable=False)
    driver_id = Column(String(120), ForeignKey("drivers.id"), nullable=False)
    restaurant_id = Column(String(120), ForeignKey("restaurants.id"),
                           nullable=False)
    delivered = Column(Boolean, nullable=False, default=False)
    destination_latitude = Column(Float, nullable=False)
    destination_longitude = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    dishes = relationship("Association", backref="order")

    def add_dish_to_order(self, dish):
        """Adds a dish to the order"""
        if isinstance(dish, Dish):
            self.save()
            assoc = Association(extra_data="TODO")
            assoc.order_id = self.id
            assoc.dish_id = dish.id
            models.db.new(assoc)
            models.db.save()

