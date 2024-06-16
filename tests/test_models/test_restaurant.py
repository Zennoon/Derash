#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    TestRestaurantAttrs - Unittest tests for the Restaurant class's attributes

    TestRestaurantDB - Unittest tests for Restaurant class operations that involve db
"""
import unittest

from models import db
from models.owner import Owner
from models.restaurant import Restaurant


class TestRestaurantAttrs(unittest.TestCase):
    """Test cases for the Restaurant class attributes"""
    def setUp(self):
        """Executed before each test/method"""
        self.restaurant = Restaurant()

    def test_name(self):
        """Tests the name attribute of the class"""
        self.assertTrue(hasattr(Restaurant, "name"))
        self.restaurant.name = "McDonalds"
        self.assertEqual(self.restaurant.name, "McDonalds")

    def test_description(self):
        """Tests the description attribute of the class"""
        self.assertTrue(hasattr(Restaurant, "description"))
        desc = "Plain old McDonalds"
        self.restaurant.description = desc
        self.assertEqual(self.restaurant.description, desc)

    def test_owner_id(self):
        """Tests the owner_id attribute of the class"""
        self.assertTrue(hasattr(Restaurant, "owner_id"))
        my_owner = Owner()
        self.restaurant.owner_id = my_owner.id
        self.assertEqual(self.restaurant.owner_id, my_owner.id)

    def test_latitude(self):
        """Tests the latitude attribute of the class"""
        self.assertTrue(hasattr(Restaurant, "latitude"))
        self.restaurant.latitude = 12.2334
        self.assertEqual(self.restaurant.latitude, 12.2334)

    def test_longitude(self):
        """Tests the longitude attribute of the class"""
        self.assertTrue(hasattr(Restaurant, "longitude"))
        self.restaurant.longitude = 12.2334
        self.assertEqual(self.restaurant.longitude, 12.2334)

class TestRestaurantDB(unittest.TestCase):
    """
    Test cases for the Restaurant class operations
    involving the database
    """
    def setUp(self):
        """Executed before each test/method"""
        self.owner = Owner(first_name="Dora", last_name="TheExplorer",
                         email="swiper@hater.com", password="B00t5",
                         phone_num="0918273645")
        self.owner.save()
        self.restaurant = Restaurant(name="Sushi Place", description="Serves Sushi",
                                     latitude=43.3452, longitude=34.4325,
                                     owner_id=self.owner.id)

    def tearDown(self):
        """Executed after each test/method"""
        self.restaurant.delete()
        self.owner.delete()

    def test_save(self):
        """Tests the save method of the class"""
        self.restaurant.save()
        my_restaurant = db.get(Restaurant, self.restaurant.id)
        self.assertIs(self.restaurant, my_restaurant)

    def test_delete(self):
        """Tests the delete method of the class"""
        self.restaurant.save()
        
        my_restaurant = Restaurant()
        my_restaurant.name = "The Chinese Place"
        my_restaurant.description = "All you can eat buffet"
        my_restaurant.owner_id = self.owner.id
        my_restaurant.latitude = 34.2516
        my_restaurant.longitude = 61.5243
        
        my_restaurant.save()
        my_restaurant2 = db.get(Restaurant, my_restaurant.id)
        self.assertIs(my_restaurant, my_restaurant2)
        my_restaurant.delete()
        my_restaurant2 = db.get(Restaurant, my_restaurant.id)
        self.assertIsNone(my_restaurant2)

    def test_owner(self):
        """Test the owner query of the class"""
        self.restaurant.save()
        self.assertIs(self.restaurant.owner, self.owner)
        self.assertTrue(self.restaurant in self.owner.restaurants)

