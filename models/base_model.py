#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    BaseModel - Parent class for all the concrete classes.
    Contains all the common attributes
"""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_base

import models


Base = declarative_base()


class BaseModel():
    """Base class for other classes to inherit from"""
    id = Column(String(120), primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    def __init__(self, *args, **kwargs):
        """Initializes a new instance"""
        self.id = str(uuid4()) + str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs is not None:
            for key in kwargs:
                if key not in ["id", "created_at", "updated_at"]:
                    self.__dict__[key] = kwargs[key]

    def __str__(self):
        """Informal string representation of the instance"""
        dct = self.__dict__.copy()
        if dct.get("_sa_instance_state") is not None:
            dct.pop("_sa_instance_state")
        if dct.get("password") is not None:
            dct.pop("password")
        c_name = self.__class__.__name__
        args = ["{}={}".format(key, val) for key, val in dct.items()]
        return f"{c_name}({', '.join(args)})"

    def to_dict(self):
        """Dictionary representation of the instance"""
        dct = self.__dict__.copy()
        dct["created_at"] = dct["created_at"].isoformat()
        dct["updated_at"] = dct["updated_at"].isoformat()
        if dct.get("_sa_instance_state") is not None:
            del dct["_sa_instance_state"]
        if dct.get("password") is not None:
            dct.pop("password")
        return (dct)

    def save(self):
        """Commit the instance to the storage session"""
        models.db.new(self)
        models.db.save()

    def delete(self):
        """Delete instance from storage"""
        models.db.delete(self)
