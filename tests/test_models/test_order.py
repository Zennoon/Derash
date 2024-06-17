#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    TestOrderAttrs - Unittest tests for the Order class's attributes

    TestOrderDB - Unittest tests for Order class operations that involve db
"""
import unittest

from models import db
from models.customer import Customer
from models.driver import Driver
from models.dish import Dish
from models.order import Order, Association
from models.owner import Owner
from models.restaurant import Restaurant


class TestOrderAttrs(unittest.TestCase):
    """Test cases for the Order class attributes"""
    def setUp(self):
        """Executed before each test/method"""
        self.order = Order()

    def test_customer_id(self):
        """Tests the customer_id attribute of the class"""
        self.assertTrue(hasattr(self.order, "customer_id"))
        customer = Customer()
        self.order.customer_id = customer.id
        self.assertEqual(self.order.customer_id, customer.id)

    def test_driver_id(self):
        """Tests the driver_id attribute of the class"""
        self.assertTrue(hasattr(self.order, "driver_id"))
        driver = Driver()
        self.order.driver_id = driver.id
        self.assertEqual(self.order.driver_id, driver.id)

    def test_restaurant_id(self):
        """Tests the restaurant_id attribute of the class"""
        self.assertTrue(hasattr(self.order, "restaurant_id"))
        restaurant = Restaurant()
        self.order.restaurant_id = restaurant.id
        self.assertEqual(self.order.restaurant_id, restaurant.id)

    def test_delivered(self):
        """Tests the delivered attribute of the class"""
        self.assertTrue(self.order, "delivered")
        self.assertFalse(self.order.delivered)
        self.order.delivered = True
        self.assertTrue(self.order.delivered)

    def test_destination_latitude(self):
        """Tests the destination_latitude attribute of the class"""
        self.assertTrue(self.order, "destination_latitude")
        self.order.destination_latitude = 16.2534
        self.assertEqual(self.order.destination_latitude, 16.2534)

    def test_destination_longitude(self):
        """Tests the destination_longitude attribute of the class"""
        self.assertTrue(self.order, "destination_longitude")
        self.order.destination_longitude = 34.2516
        self.assertEqual(self.order.destination_longitude, 34.2516)

    def test_dishes(self):
        """Tests the dishes attribute of the class"""

    def test_price(self):
        """Tests the price attribute of the class"""
        self.assertTrue(self.order, "price")
        self.order.price = 125.45
        self.assertEqual(self.order.price, 125.45)

    
class TestOrderDB(unittest.TestCase):
    """Test casesfor Order class operations involving database"""
    def setUp(self):
        """Executed before each test/method"""
        self.customer = Customer(first_name="Ginger", last_name="Breadman",
                                 email="ginger@islovely.com", password="Garlic@intshit",
                                 phone_num="0913243546")
        self.customer.save()

        self.driver = Driver(first_name="Huey", last_name="Freeman",
                             email="domestic@terrorist.com", password="R1leY&GrandDaD",
                             phone_num="0909080706", license_num="B17327")
        self.driver.save()

        self.owner = Owner(first_name="Dora", last_name="TheExplorer",
                         email="swiper@hater.com", password="B00t5",
                         phone_num="0918273645")
        self.owner.save()

        self.restaurant = Restaurant(name="Sushi Place", description="Serves Sushi",
                                     latitude=43.3452, longitude=34.4325,
                                     owner_id=self.owner.id)
        self.restaurant.save()

        self.dish = Dish(name="Sushi", description="Plain Sushi",
                         restaurant_id=self.restaurant.id, ingredients="Fish",
                         price=24.50)
        self.dish.save()

        self.order = Order(customer_id=self.customer.id, driver_id=self.driver.id,
                           restaurant_id=self.restaurant.id,
                           destination_latitude=12.3456, destination_longitude=65.4321,
                           price=24.90)
        
    def tearDown(self):
        """Executed after each test/method"""
        self.order.delete()
        self.customer.delete()
        self.driver.delete()
        self.owner.delete()

    def test_save(self):
        """Tests the save method of the class"""
        self.order.save()
        my_order = db.get(Order, self.order.id)
        self.assertIs(self.order, my_order)

    def test_delete(self):
        """Tests the delete method of the class"""
        self.order.save()
        
        my_order = Order()
        my_order.customer_id = self.customer.id
        my_order.driver_id = self.driver.id
        my_order.restaurant_id = self.restaurant.id
        my_order.destination_latitude = 12.3456
        my_order.destination_longitude = 65.4321
        my_order.price = 24.90
        my_order.save()
        
        my_order2 = db.get(Order, my_order.id)
        self.assertIs(my_order, my_order2)
        my_order.delete()
        my_order2 = db.get(Order, my_order.id)
        self.assertIsNone(my_order2)

    def test_customer(self):
        """Test the customer query of the class"""
        self.order.save()
        self.assertIs(self.order.customer, self.customer)
        self.assertTrue(self.order in self.customer.all_orders)

    def test_driver(self):
        """Tests the driver query of the class"""
        self.order.save()
        self.assertIs(self.order.driver, self.driver)
        self.assertTrue(self.order in self.driver.all_orders)

    def test_restaurant(self):
        """Tests the restaurant query of the class"""
        self.order.save()
        self.assertIs(self.order.restaurant, self.restaurant)
        self.assertTrue(self.order in self.restaurant.all_orders)

    def test_add_dishes_to_order(self):
        """Tests the add_dishes_to_order method of the class"""
        self.order.add_dish_to_order(self.dish)
        self.assertIsInstance(self.order.dishes, list)
        self.assertIsInstance(self.order.dishes[0], Association)
        self.assertIsInstance(self.order.dishes[0].dish, Dish)
        self.assertIs(self.order.dishes[0].dish, self.dish)

        self.order.add_dish_to_order(self.dish)
        self.assertEqual(len(self.order.dishes), 2)
        for assoc in self.order.dishes:
            self.assertIs(assoc.dish, self.dish)