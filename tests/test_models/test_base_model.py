#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    TestBaseModel - Unittest tests for the BaseModel class
"""
import unittest
from datetime import datetime

from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test cases for the BaseModel class"""

    def setUp(self):
        """Executed before every test/method"""
        self.base_model = BaseModel()

    def tearDown(self):
        """Executed after every test/method"""
        del self.base_model

    def test_class(self):
        """Tests that the class is imported and instances can be created"""
        self.assertEqual(BaseModel.__class__.__name__, "type")
        self.assertIsInstance(self.base_model, BaseModel)

    def test_id(self):
        """Tests the id attribute of the class"""
        self.assertTrue(hasattr(self.base_model, "id"))
        self.assertIsInstance(self.base_model.id, str)
        base_model2 = BaseModel()
        self.assertNotEqual(self.base_model.id, base_model2.id)

    def test_created_at(self):
        """Tests the created_at attribute of the class"""
        self.assertTrue(hasattr(self.base_model, "created_at"))
        self.assertIsInstance(self.base_model.created_at, datetime)

    def test_updated_at(self):
        """Tests the updated_at attribute of the class"""
        self.assertTrue(hasattr(self.base_model, "updated_at"))
        self.assertIsInstance(self.base_model.updated_at, datetime)

    def test_str(self):
        """Tests the __str__ method of the class"""
        dct = self.base_model.__dict__.copy()
        if dct.get("_sa_instance_state") is not None:
            dct.pop("_sa_instance_state")
        if dct.get("password") is not None:
            dct.pop("password")
        c_name = self.base_model.__class__.__name__
        args = ["{}={}".format(key, val) for key, val in dct.items()]
        correct_output = "{}({})".format(c_name, ", ".join(args))
        self.assertEqual(str(self.base_model), correct_output)

    def test_to_dict(self):
        """Tests the to_dict method of the class"""
        dct = self.base_model.__dict__.copy()
        dct["created_at"] = dct["created_at"].isoformat()
        dct["updated_at"] = dct["updated_at"].isoformat()
        if dct.get("_sa_instance_state") is not None:
            dct.pop("_sa_instance_state")
        if dct.get("password") is not None:
            dct.pop("password")
        self.assertDictEqual(self.base_model.to_dict(), dct)
