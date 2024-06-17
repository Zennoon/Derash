#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    DBStorage - Establishes connection and provides access to the derash_db database
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.base_model import Base
from models.customer import Customer
from models.dish import Dish
from models.driver import Driver
from models.order import Association
from models.order import Order
from models.owner import Owner
from models.restaurant import Restaurant
from models.review import Review


classes = [Customer, Dish, Driver, Order, Owner, Restaurant, Review]


class DBStorage():
    """Gives access to the MySQL database holding application data"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the instance"""
        if os.getenv("DERASH_ENV") == "test":
            db_name = "derash_test_db"
        else:
            db_name = "derash_db"
        db_user = "derash_db_user"
        db_pwd = os.getenv("DERASH_DB_PWD")
        db_host = "localhost"
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(db_user,
                                                                           db_pwd,
                                                                           db_host,
                                                                           db_name))
        
    def reload(self):
        """Creates a session and loads all tables"""
        if os.getenv("DERASH_ENV") == "test":
            Base.metadata.drop_all(bind=self.__engine)
        Base.metadata.create_all(bind=self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def new(self, obj):
        """Adds a new object to the current session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes added in the current session to the database"""
        self.__session.commit()

    def get(self, cls, id):
        """Retrieves an object of the given class and with the given id from the database"""
        obj = self.__session.query(cls).filter(cls.id == id).all()
        if obj == []:
            return (None)
        return (obj[0])
    
    def filter_by_attr(self, cls, attr, val):
        """Retrieves object(s) from database after filtering using an attribute value"""
        objs = self.__session.query(cls).filter(cls.__dict__.get(attr) == val).all()
        return (objs)

    def delete(self, obj):
        """Deletes an object from the database"""
        self.__session.delete(obj)
        self.save()

    def all(self, cls=None):
        """Retrieves all instances of given class or all objects if class not given"""
        all_objs = []
        if cls is None:
            for cl in classes:
                all_objs.extend(self.__session.query(cl).all())
        else:
            all_objs = self.__session.query(cls).all()
        return (all_objs)



    def close(self):
        """Renews session. To be used after transactions"""
        self.__session.remove()

