#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    TestDriver - Unittest tests for the Driver class
"""
import unittest

from models import db
from models.driver import Driver


class TestDriver(unittest.TestCase):
    """Test cases for the Driver class"""
    def setUp(self):
        """Executed before each test/method"""
        self.driver = Driver(first_name="Calvin", last_name="Klien",
                             email="thepants@guy.com", password="Il0vePan7s.",
                             phone_num="0912345678")

    def tearDown(self):
        """Executed after each test/method"""
        self.driver.delete()

    def test_license_num(self):
        """Tests the license_num attribute of the class"""
        self.assertTrue(hasattr(self.driver, "license_num"))
        self.driver.license_num = "B17327"
        self.assertEqual(self.driver.license_num, "B17327")
        self.driver.save()

    def test_latitude(self):
        """Tests the latitude attribute of the class"""
        self.assertTrue(hasattr(self.driver, "latitude"))
        self.driver.latitude = 12.3456
        self.assertEqual(self.driver.latitude, 12.3456)
        self.driver.license_num = "B17327"
        self.driver.save()

    def test_longitude(self):
        """Tests the longitude attribute of the class"""
        self.assertTrue(hasattr(self.driver, "longitude"))
        self.driver.longitude = 65.4321
        self.assertEqual(self.driver.longitude, 65.4321)
        self.driver.license_num = "B17327"
        self.driver.save()

    def test_active(self):
        """Tests the active attribute of the class"""
        self.assertTrue(self.driver, "active")
        self.assertFalse(self.driver.active)
        self.driver.active = True
        self.assertTrue(self.driver.active)
        self.driver.license_num = "B17327"
        self.driver.save()

    def test_delivering(self):
        """Tests the delivering attribute of the Class"""
        self.assertTrue(self.driver, "delivering")
        self.assertFalse(self.driver.delivering)
        self.driver.delivering = True
        self.assertTrue(self.driver.delivering)
        self.driver.license_num = "B17327"
        self.driver.save()

    def test_save(self):
        """Tests the save method of the class"""
        self.driver.license_num = "B50043"

        self.driver.save()
        my_driver = db.get(Driver, self.driver.id)
        self.assertIs(self.driver, my_driver)

    def test_delete(self):
        """Tests the delete method of the class"""
        self.driver.license_num = "B50043"
        self.driver.save()

        my_driver = Driver()
        my_driver.first_name = "Barry"
        my_driver.last_name = "Allen"
        my_driver.email = "barry@fastest1.com"
        my_driver.password = "FlASh."
        my_driver.phone_num = "0912345678"
        my_driver.license_num = "B50044"

        my_driver.save()
        my_driver2 = db.get(Driver, my_driver.id)
        self.assertIs(my_driver, my_driver2)
        my_driver.delete()
        my_driver2 = db.get(Driver, my_driver.id)
        self.assertIsNone(my_driver2)
