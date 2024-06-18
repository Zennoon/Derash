#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    TestOwner - Unittest tests for the BaseModel class
"""
import unittest

from models import db
from models.owner import Owner


class TestOwner(unittest.TestCase):
    """Test cases for the Owner class"""
    def setUp(self):
        """Executed before each test/method"""
        self.owner = Owner()

    def tearDown(self):
        """Executed after each test/method"""
        self.owner.delete()

    def test_save(self):
        """Tests the save method of the class"""
        self.owner.first_name = "Barry"
        self.owner.last_name = "Allen"
        self.owner.email = "barry@fastest1.com"
        self.owner.password = "FlASh."
        self.owner.phone_num = "0912345678"

        self.owner.save()
        my_owner = db.get(Owner, self.owner.id)
        self.assertIs(self.owner, my_owner)

    def test_delete(self):
        """Tests the delete method of the class"""
        self.owner.first_name = "Barry"
        self.owner.last_name = "Allen"
        self.owner.email = "barry@fastest.com"
        self.owner.password = "FlASh."
        self.owner.phone_num = "0912345678"
        self.owner.save()

        my_owner = Owner()
        my_owner.first_name = "Barry"
        my_owner.last_name = "Allen"
        my_owner.email = "barry@fastest1.com"
        my_owner.password = "FlASh."
        my_owner.phone_num = "0912345678"

        my_owner.save()
        my_owner2 = db.get(Owner, my_owner.id)
        self.assertIs(my_owner, my_owner2)
        my_owner.delete()
        my_owner2 = db.get(Owner, my_owner.id)
        self.assertIsNone(my_owner2)
