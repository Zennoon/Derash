#!/usr/bin/python3
"""
Contains:
    Misc
    ====
    db - A DBStorage instance giving us access to the database storage
"""
from models.engine.db_storage import DBStorage


db = DBStorage()
default_pics = ["default_{}".format(i) for i in range(10)]
