#!/usr/bin/python3
"""
Contains:
    Misc
    ====
    db - A DBStorage instance giving us access to the database storage
"""
from derash.models.engine.db_storage import DBStorage


db = DBStorage()
db.reload()
