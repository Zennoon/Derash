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

import derash.models
from derash.models.base_model import Base, BaseModel
from derash.models.dish import Dish
from utils import calc_distance


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
    customer_confirm = Column(Boolean, nullable=False, default=False)
    driver_confirm = Column(Boolean, nullable=False, default=False)
    restaurant_confirm = Column(Boolean, nullable=False, default=False)
    destination_latitude = Column(Float, nullable=False)
    destination_longitude = Column(Float, nullable=False)
    price = Column(Float, nullable=False, default=0)
    delivery_fee = Column(Float, nullable=False, default=0)
    dishes = relationship("Association", backref="order")

    def add_dish_to_order(self, dish):
        """Adds a dish to the order"""
        if isinstance(dish, Dish):
            self.save()
            assoc = Association(extra_data="TODO")
            assoc.order_id = self.id
            assoc.dish_id = dish.id
            derash.models.db.new(assoc)
            derash.models.db.save()

    def calc_delivery_price(self):
        """Calculates the cost of delivery"""
        delivery_coords = (self.destination_latitude,
                           self.destination_longitude)
        restaurant = self.restaurant
        rest_coords = (restaurant.latitude,
                       restaurant.longitude)
        distance = calc_distance(delivery_coords, rest_coords)
        self.delivery_fee = 50 + float(int(distance * 15))

    def calc_order_price(self):
        """Calculates and assigns the total price of the order"""
        self.price = 0
        self.save()
        for assoc in self.dishes:
            self.price += assoc.dish.price
        self.save()
