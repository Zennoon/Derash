#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    TestUser - Unittest tests for the User class
"""
import unittest

from models.user import User


class TestUser(unittest.TestCase):
    """Test cases for the User class"""
    def setUp(self):
        """Executed before every test/method"""
        self.user = User()
    
    def tearDown(self):
        """Executed after every test/method"""
        del self.user

    def test_first_name(self):
        """Tests the first name attribute of the class"""
        self.assertTrue(hasattr(self.user, "first_name"))
        self.user.first_name = "Abraham"
        self.assertEqual(self.user.first_name, "Abraham")

    def test_last_name(self):
        """Tests the last name attribute of the class"""
        self.assertTrue(hasattr(self.user, "last_name"))
        self.user.last_name = "Lincoln"
        self.assertEqual(self.user.last_name, "Lincoln")

    def test_email(self):
        """Tests the email attribute of the class"""
        self.assertTrue(hasattr(self.user, "email"))
        self.user.email = "abraham.lincoln@usa.com"
        self.assertEqual(self.user.email, "abraham.lincoln@usa.com")

    def test_password(self):
        """Tests the password attribute of the class"""
        self.assertTrue(hasattr(self.user, "password"))
        self.user.password = "L1nC@lN"
        self.assertEqual(self.user.password, "L1nC@lN")
        
    def test_phone_num(self):
        """Tests the phone_num attribute of the class"""
        self.assertTrue(hasattr(self.user, "phone_num"))
        self.user.phone_num = "0912345678"
        self.assertEqual(self.user.phone_num, "0912345678")
