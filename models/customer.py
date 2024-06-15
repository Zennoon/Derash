#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    Customer - A concrete class representing a user who orders
"""
from sqlalchemy.orm import relationship

from models.base_model import Base
from models.order import Order
from models.review import Review
from models.user import User


class Customer(User, Base):
    """A user who makes orders"""
    __tablename__ = "customers"
    all_orders = relationship("Order", backref="customer")
    reviews = relationship("Review", backref="customer",
                           cascade="all, delete, delete-orphan")

    def get_pending_orders(self):
        """Returns the pending orders of the customer"""
        return (list(filter(lambda order: order.delivered is False,
                            self.all_orders)))
