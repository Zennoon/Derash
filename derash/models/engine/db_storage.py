#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    DBStorage - Establishes connection and provides access to the
    derash_db database
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from derash.models.base_model import Base
from derash.models.customer import Customer
from derash.models.dish import Dish
from derash.models.driver import Driver
from derash.models.order import Association
from derash.models.order import Order
from derash.models.owner import Owner
from derash.models.restaurant import Restaurant
from derash.models.review import Review
from derash.models.user import User


classes = [Customer, Dish, Driver, Order, Owner, Restaurant, Review]
users = [Customer, Driver, Owner]


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
        conn_cmd = "mysql+mysqldb://{}:{}@{}/{}"
        self.__engine = create_engine(conn_cmd.format(db_user, db_pwd,
                                                      db_host, db_name))

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
        """
        Retrieves an object of the given class and with the given id
        from the database
        """
        if cls is User:
            obj = []
            for cl in users:
                obj.extend(self.__session.query(cl).filter(cl.id == id).all())
        else:
            obj = self.__session.query(cls).filter(cls.id == id).all()
        if obj == []:
            return (None)
        return (obj[0])

    def filter_by_attr(self, cls, attr, val):
        """
        Retrieves object(s) from database after filtering using
        an attribute value
        """
        if cls is User:
            objs = []
            for cl in users:
                q = self.__session.query(cl).filter(
                    cl.__dict__.get(attr) == val
                    )
                objs.extend(q.all())
        else:
            q = self.__session.query(cls).filter(cls.__dict__.get(attr) == val)
            objs = q.all()
        return (objs)

    def delete(self, obj):
        """Deletes an object from the database"""
        self.__session.delete(obj)
        self.save()

    def all(self, cls=None):
        """
        Retrieves all instances of given class or
        all objects if class not given
        """
        all_objs = []
        if cls is None:
            for cl in classes:
                all_objs.extend(self.__session.query(cl).all())
        else:
            if cls is User:
                for cl in users:
                    all_objs.extend(self.__session.query(cl).all())
            else:
                all_objs = self.__session.query(cls).all()
        return (all_objs)

    def close(self):
        """Renews session. To be used after transactions"""
        self.__session.remove()
