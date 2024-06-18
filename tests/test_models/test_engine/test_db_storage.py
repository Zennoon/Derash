#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    TestDBStorage - unittest tests for the DBStorage class
"""
import os
import unittest

from sqlalchemy import inspect

from models.customer import Customer
from models.dish import Dish
from models.driver import Driver
from models.order import Order
from models.owner import Owner
from models.restaurant import Restaurant
from models.review import Review
from models.user import User
from models.engine.db_storage import DBStorage


class TestDBStorage(unittest.TestCase):
    """Test cases for the DBStorage class"""
    def setUp(self):
        """Executed before each test/method"""
        self.db = DBStorage()
        self.db.reload()

    def tearDown(self):
        """Executed after each test/method"""
        self.db.close()

    def test_private_attrs(self):
        """Tests that the private attributes are actually private"""
        with self.assertRaises(AttributeError):
            engine = self.db.__engine
        with self.assertRaises(AttributeError):
            session = self.db.__session

    def test_new(self):
        """Tests the new method of the class"""
        customer = Customer(first_name="Alexander", last_name="Thegreat",
                            email="thealex@gmail.com", password="password1",
                            phone_num="0912345678")
        self.db.new(customer)
        self.assertFalse(inspect(customer).detached)

    def test_save(self):
        """Tests the save method of the class"""
        length = len(self.db.all())
        customer = Customer(first_name="Alexander", last_name="Thegreat",
                            email="thealex@gmail.com", password="password1",
                            phone_num="0912345678")
        self.db.new(customer)
        self.db.save()
        self.assertEqual(len(self.db.all()), length + 1)
        self.db.delete(customer)

    def test_get(self):
        """Tests the get method of the class"""
        owner_1 = Owner(first_name="Alexander", last_name="Thegreat",
                        email="thealex@gmail.com", password="password1",
                        phone_num="0912345678")
        self.db.new(owner_1)
        self.db.save()

        owner_2 = Owner(first_name="Bobby", last_name="Fischer",
                        email="bobby@chess.com", password="password2",
                        phone_num="0921436587")
        self.db.new(owner_2)
        self.db.save()

        my_owner = self.db.get(Owner, owner_1.id)
        self.assertIs(owner_1, my_owner)

        my_owner = self.db.get(Owner, owner_2.id)
        self.assertIs(owner_2, my_owner)

        self.db.delete(owner_1)
        self.db.delete(owner_2)

    def test_get_invalid_id(self):
        """Tests the get method with an ID that doesn't exist"""
        my_owner = self.db.get(Owner, "12345")
        self.assertIsNone(my_owner)

    def test_filter_by_attr(self):
        """Tests the filter_by_attr method of the class"""
        driver_1 = Driver(first_name="Alexander", last_name="Thegreat",
                          email="thealex@gmail.com", password="password3",
                          phone_num="0912345678", license_num="B17327")
        self.db.new(driver_1)
        self.db.save()

        driver_2 = Driver(first_name="Catherine", last_name="Zeigel",
                          email="cathie@gmail.com", password="password3",
                          phone_num="0987654321", license_num="B72371")
        self.db.new(driver_2)
        self.db.save()

        my_driver = self.db.filter_by_attr(Driver, "first_name", "Alexander")
        my_driver = my_driver[0]
        self.assertIs(my_driver, driver_1)

        my_driver = self.db.filter_by_attr(Driver, "license_num", "B72371")[0]
        self.assertIs(my_driver, driver_2)

        my_drivers = self.db.filter_by_attr(Driver, "password", "password3")
        for driver in [driver_1, driver_2]:
            self.assertTrue(driver in my_drivers)

        self.db.delete(driver_1)
        self.db.delete(driver_2)

    def test_filter_by_attr_user(self):
        """Tests the filter_by_attr method with the User class"""
        customer = Customer(first_name="Alexander", last_name="Thegreat",
                            email="thealex@gmail.com", password="password1",
                            phone_num="0912345678")
        self.db.new(customer)
        self.db.save()

        owner = Owner(first_name="Baresi", last_name="Franco",
                      email="baresi@baller.com", password="password2",
                      phone_num="0911223344")
        self.db.new(owner)
        self.db.save()

        driver = Driver(first_name="Catherine", last_name="Zeigel",
                        email="cathie@gmail.com", password="password3",
                        phone_num="0987654321", license_num="B72371")
        self.db.new(driver)
        self.db.save()

        my_user = self.db.filter_by_attr(User, "email", "cathie@gmail.com")[0]
        self.assertIs(my_user, driver)

        self.db.delete(customer)
        self.db.delete(owner)
        self.db.delete(driver)

    def test_filter_by_attr_invalid_val(self):
        """
        Tests the filter_by_attr method with an attr value
        that doesn't exist
        """
        customer = Customer(first_name="Alexander", last_name="Thegreat",
                            email="thealex@gmail.com", password="password1",
                            phone_num="0912345678")
        self.db.new(customer)
        self.db.save()

        obj = self.db.filter_by_attr(Customer, "email", "this@doesnt.exist")
        self.assertEqual(obj, [])
        self.db.delete(customer)

    def test_filter_by_attr_invalid_attr(self):
        """Tests the filter_by_attr method with an attr that doesn't exist"""
        customer = Customer(first_name="Alexander", last_name="Thegreat",
                            email="thealex@gmail.com", password="password1",
                            phone_num="0912345678")
        self.db.new(customer)
        self.db.save()

        obj = self.db.filter_by_attr(Customer, "doesn't exist", "random_val")
        self.assertEqual(obj, [])
        self.db.delete(customer)

    def test_all(self):
        """Tests the all method of the class"""
        customer = Customer(first_name="Alexander", last_name="Thegreat",
                            email="thealex@gmail.com", password="password1",
                            phone_num="0912345678")
        self.db.new(customer)
        self.db.save()

        owner = Owner(first_name="Baresi", last_name="Franco",
                      email="baresi@baller.com", password="password2",
                      phone_num="0911223344")
        self.db.new(owner)
        self.db.save()

        driver = Driver(first_name="Catherine", last_name="Zeigel",
                        email="cathie@gmail.com", password="password3",
                        phone_num="0987654321", license_num="B72371")
        self.db.new(driver)
        self.db.save()

        restaurant = Restaurant(name="Sushi Place",
                                description="Sublime Sushi",
                                latitude=23.4532, longitude=54.3245,
                                owner_id=owner.id)
        self.db.new(restaurant)
        self.db.save()

        objs = self.db.all(Owner)
        self.assertIs(owner, objs[0])
        for obj in [customer, driver, restaurant]:
            self.assertFalse(obj in objs)

        objs = self.db.all()
        self.assertEqual(len(objs), 4)
        for obj in [customer, driver, owner, restaurant]:
            self.assertTrue(obj in objs)

        for obj in [customer, restaurant, owner, driver]:
            self.db.delete(obj)

    def test_all_user(self):
        """Tests the all method with the User class"""
        customer = Customer(first_name="Alexander", last_name="Thegreat",
                            email="thealex@gmail.com", password="password1",
                            phone_num="0912345678")
        self.db.new(customer)
        self.db.save()

        owner = Owner(first_name="Baresi", last_name="Franco",
                      email="baresi@baller.com", password="password2",
                      phone_num="0911223344")
        self.db.new(owner)
        self.db.save()

        driver = Driver(first_name="Catherine", last_name="Zeigel",
                        email="cathie@gmail.com", password="password3",
                        phone_num="0987654321", license_num="B72371")
        self.db.new(driver)
        self.db.save()

        restaurant = Restaurant(name="Sushi Place",
                                description="Sublime Sushi",
                                latitude=23.4532, longitude=54.3245,
                                owner_id=owner.id)
        self.db.new(restaurant)
        self.db.save()

        objs = self.db.all(User)
        self.assertEqual(len(objs), 3)
        for obj in [customer, driver, owner]:
            self.assertTrue(obj in objs)
        self.assertFalse(restaurant in objs)

        for obj in [customer, restaurant, owner, driver]:
            self.db.delete(obj)

    def test_delete(self):
        """Tests the delete method of the class"""
        customer_1 = Customer(first_name="Alexander", last_name="Thegreat",
                              email="thealex@gmail.com", password="password1",
                              phone_num="0912345678")
        self.db.new(customer_1)
        self.db.save()

        customer_2 = Customer(first_name="Captain", last_name="America",
                              email="ironmain@aint.shit", password="password2",
                              phone_num="0919283746")
        self.db.new(customer_2)
        self.db.save()

        customers = self.db.all(Customer)
        self.assertEqual(len(customers), 2)

        self.db.delete(customer_1)

        customers = self.db.all(Customer)
        self.assertEqual(len(customers), 1)
        self.assertIsNone(self.db.get(Customer, customer_1.id))

        self.db.delete(customer_2)

        customers = self.db.all(Customer)
        self.assertEqual(len(customers), 0)
        self.assertIsNone(self.db.get(Customer, customer_2.id))
