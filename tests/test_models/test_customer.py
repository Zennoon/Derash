#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    TestCustomer - Unittest tests for the Customer class
"""
import unittest

from models import db
from models.customer import Customer


class TestCustomer(unittest.TestCase):
    """Test cases for the Customer class"""
    def setUp(self):
        """Executed before each test/method"""
        self.customer = Customer()

    def tearDown(self):
        """Executed after each test/method"""
        self.customer.delete()

    def test_save(self):
        """Tests the save method of the class"""

        self.customer.first_name = "Barry"
        self.customer.last_name = "Allen"
        self.customer.email = "barry@fastest1.com"
        self.customer.password = "FlASh."
        self.customer.phone_num = "0912345678"

        self.customer.save()
        my_customer = db.get(Customer, self.customer.id)
        self.assertIs(self.customer, my_customer)

    def test_delete(self):
        """Tests the delete method of the class"""
        self.customer.first_name = "Barry"
        self.customer.last_name = "Allen"
        self.customer.email = "barry@fastest.com"
        self.customer.password = "FlASh."
        self.customer.phone_num = "0912345678"
        self.customer.save()

        my_customer = Customer()
        my_customer.first_name = "Barry"
        my_customer.last_name = "Allen"
        my_customer.email = "barry@fastest1.com"
        my_customer.password = "FlASh."
        my_customer.phone_num = "0912345678"

        my_customer.save()
        my_customer2 = db.get(Customer, my_customer.id)
        self.assertIs(my_customer, my_customer2)
        my_customer.delete()
        my_customer2 = db.get(Customer, my_customer.id)
        self.assertIsNone(my_customer2)
