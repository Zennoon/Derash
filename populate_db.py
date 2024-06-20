#!/usr/bin/python3
"""
Populates database with mock data
"""
import json
import random

from models import db
from models.customer import Customer
from models.dish import Dish
from models.driver import Driver
from models.order import Order
from models.owner import Owner
from models.restaurant import Restaurant
from models.review import Review


def get_random_elem(lst):
    """Returns a random element from a list"""
    return lst[random.randint(0, len(lst) - 1)]

# with open("./mock_cust_owner.json") as f:
#     dcts = json.load(f)
#     for idx, dct in enumerate(dcts):
#         if idx % 2:
#             customer = Customer(**dct)
#             customer.save()
#         else:
#             owner = Owner(**dct)
#             owner.save()

# with open("./mock_driver.json") as f:
#     dcts = json.load(f)
#     for dct in dcts:
#         driver = Driver(**dct)
#         driver.save()

# with open("./mock_rest.json") as f:
#     dcts = json.load(f)
#     owners = db.all(Owner)
#     for dct in dcts:
#         restaurant = Restaurant(**dct)
#         restaurant.owner_id = get_random_elem(owners).id
#         restaurant.save()

with open("./mock_dish.json") as f:
    dcts = json.load(f)
    restaurants = db.all(Restaurant)
    for dct in dcts:
        dish = Dish(**dct)
        dish.restaurant_id = get_random_elem(restaurants).id
        dish.save()

with open("./mock_review.json") as f:
    dcts = json.load(f)
    customers = db.all(Customer)
    restaurants = db.all(Restaurant)
    for dct in dcts:
        review = Review(**dct)
        review.customer_id = get_random_elem(customers).id
        review.restaurant_id = get_random_elem(restaurants).id
        review.save()

with open("./mock_order.json") as f:
    dcts = json.load(f)
    customers = db.all(Customer)
    restaurants = db.all(Restaurant)
    drivers = db.all(Driver)
    for dct in dcts:
        order = Order(**dct)
        order.customer_id = get_random_elem(customers).id
        order.driver_id = get_random_elem(drivers).id
        restaurant = get_random_elem(restaurants)
        order.restaurant_id = restaurant.id
        dishes = restaurant.dishes
        rand = random.randint(1, 5)
        for i in range(rand):
            dish = get_random_elem(dishes)
            order.add_dish_to_order(dish)
        order.calc_order_price()
        order.save()

