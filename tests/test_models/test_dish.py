#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    TestDishAttrs - Unittest tests for the Dish class's attributes

    TestDishDB - Unittest tests for Dish class operations that involve db
"""
import unittest

from models import db
from models.dish import Dish
from models.owner import Owner
from models.restaurant import Restaurant


class TestDishAttrs(unittest.TestCase):
    """Test cases for the Dish class attributes"""
    def setUp(self):
        """Executed before each test/method"""
        self.dish = Dish()

    def test_name(self):
        """Tests the name attribute of the class"""
        self.assertTrue(hasattr(self.dish, "name"))
        self.dish.name = "Sushi"
        self.assertEqual(self.dish.name, "Sushi")

    def test_description(self):
        """Tests the description attribute of the class"""
        self.assertTrue(hasattr(self.dish, "description"))
        self.dish.description = "Plain Sushi"
        self.assertEqual(self.dish.description, "Plain Sushi")

    def test_restaurant_id(self):
        """Tests the restaurant_id attribute of the class"""
        self.assertTrue(hasattr(self.dish, "restaurant_id"))
        restaurant = Restaurant()
        self.dish.restaurant_id = restaurant.id
        self.assertEqual(self.dish.restaurant_id, restaurant.id)

    def test_ingredients(self):
        """Tests the ingredients attribute of the class"""
        self.assertTrue(hasattr(self.dish, "ingredients"))
        self.dish.ingredients = "Fish, Salt, Pepper"
        self.assertEqual(self.dish.ingredients, "Fish, Salt, Pepper")

    def test_price(self):
        """Tests the price attribute of the class"""
        self.assertTrue(hasattr(self.dish, "price"))
        self.dish.price = 95.50
        self.assertEqual(self.dish.price, 95.50)


class TestDishDB(unittest.TestCase):
    """Test cases for Dish class operations involving database"""
    def setUp(self):
        """Executed before each test/method"""
        self.owner = Owner(first_name="Einstien", last_name="Albert",
                           email="madgenius@atomic.com", password="e=mc^2",
                           phone_num="0930495867")
        self.owner.save()

        desc = "For legal purposes, Pizza Hot, not Hut"
        self.restaurant = Restaurant(name="Pizza Hot", description=desc,
                                     latitude=10.2938, longitude=38.4756,
                                     owner_id=self.owner.id)
        self.restaurant.save()

        self.dish = Dish(name="Pepperoni Pizza", description="Again, Hot not Hut",
                         ingredients="Pepperoni, Dough", price=12.50,
                         restaurant_id=self.restaurant.id)
        
    def tearDown(self):
        self.owner.delete()
        
    def test_save(self):
        """Tests the save method of the class"""
        self.dish.save()
        my_dish = db.get(Dish, self.dish.id)
        self.assertIs(self.dish, my_dish)

    def test_delete(self):
        """Tests the delete method of the class"""
        self.dish.save()
        
        my_dish = Dish()
        my_dish.name = "Burgerizza"
        my_dish.description = "I don't even know where to start"
        my_dish.restaurant_id = self.restaurant.id
        my_dish.ingredients = "Burger, Pizza"
        my_dish.price = 15.45
        
        my_dish.save()
        my_dish2 = db.get(Dish, my_dish.id)
        self.assertIs(my_dish, my_dish2)
        my_dish.delete()
        my_dish2 = db.get(Dish, my_dish.id)
        self.assertIsNone(my_dish2)

    def test_restaurant(self):
        """Test the restaurant query of the class"""
        self.dish.save()
        self.assertIs(self.dish.restaurant, self.restaurant)
        self.assertTrue(self.dish in self.restaurant.dishes)
