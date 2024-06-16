#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    TestReviewAttrs - Unittest tests for the Review class's attributes

    TestReviewDB - Unittest tests for Review class operations that involve db
"""
import unittest

from models import db
from models.customer import Customer
from models.owner import Owner
from models.restaurant import Restaurant
from models.review import Review


class TestReviewAttrs(unittest.TestCase):
    """Test cases for the Review class attributes"""
    def setUp(self):
        """Executed before each test/method"""
        self.review = Review()

    def test_customer_id(self):
        """Tests the customer_id attribute of the class"""
        self.assertTrue(hasattr(self.review, "customer_id"))
        customer = Customer()
        self.review.customer_id = customer.id
        self.assertEqual(self.review.customer_id, customer.id)

    def test_restaurant_id(self):
        """Tests the restaurant_id attribute of the class"""
        self.assertTrue(hasattr(self.review, "restaurant_id"))
        restaurant = Restaurant()
        self.review.restaurant_id = restaurant.id
        self.assertEqual(self.review.restaurant_id, restaurant.id)

    def test_text(self):
        """Tests the text attribute of the class"""
        self.assertTrue(hasattr(self.review, "text"))
        self.review.text = "The food was spectacular"
        self.assertEqual(self.review.text, "The food was spectacular")


class TestReviewDB(unittest.TestCase):
    """Test cases for Review class operations that involve database"""
    def setUp(self):
        """Executed before each test/method"""
        self.customer = Customer(first_name="Flint", last_name="Lockwood",
                                 email="meatballs@sphagetti.com", password="W3A7h3RGirl",
                                 phone_num="0912233445")
        self.customer.save()

        self.owner = Owner(first_name="Guy", last_name="Ritchie",
                           email="gentlemen@gypsy.com", password="FanA7ic",
                           phone_num="0913243546")
        self.owner.save()

        desc = "Just noodles and fun!"
        self.restaurant = Restaurant(name="Noodles Spot", description=desc,
                                     latitude=18.2938, longitude=28.4756,
                                     owner_id=self.owner.id)
        self.restaurant.save()

        self.review = Review(text="The noodles were supreme",
                             customer_id=self.customer.id,
                             restaurant_id=self.restaurant.id)
        
    def tearDown(self):
        """Executed after each test/method"""
        self.customer.delete()
        self.owner.delete()

    def test_save(self):
        """Tests the save method of the class"""
        self.review.save()
        my_review = db.get(Review, self.review.id)
        self.assertIs(self.review, my_review)

    def test_delete(self):
        """Tests the delete method of the class"""
        self.review.save()
        
        my_review = Review()
        my_review.text = "Awesome staff!"
        my_review.customer_id = self.customer.id
        my_review.restaurant_id = self.restaurant.id
        
        my_review.save()
        my_review2 = db.get(Review, my_review.id)
        self.assertIs(my_review, my_review2)
        my_review.delete()
        my_review2 = db.get(Review, my_review.id)
        self.assertIsNone(my_review2)

    def test_customer(self):
        """Test the customer query of the class"""
        self.review.save()
        self.assertIs(self.review.customer, self.customer)
        self.assertTrue(self.review in self.customer.reviews)
    
    def test_restaurant(self):
        """Test the restaurant query of the class"""
        self.review.save()
        self.assertIs(self.review.restaurant, self.restaurant)
        self.assertTrue(self.review in self.restaurant.reviews)
