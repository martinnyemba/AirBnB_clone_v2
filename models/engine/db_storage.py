#!/usr/bin/pythhon3
"""
This module defines a class to manage database
storage for the AirBnB_clone_v2 project
"""

from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage():
    """
    Class to manage database storage
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes the DBStorage class
        """
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query all on the current database session
        """
        all_classes = {}
        model_classes = [State, City, User, Place, Review, Amenity]
        if cls:
            query = self.__session.query(cls)
            for v in query:
                key = "{}.{}".format(v.__class__.__name__, v.id)
                all_classes[key] = v
            return all_classes

        for cls in model_classes:
            queries = self.__session.query(cls).all()
            for query in queries:
                key = "{}.{}".format(query.__class__.__name__, query.id)
                all_classes[key] = query
        return all_classes

    def new(self, obj):
        """
        Add the object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete an object from the current database session
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Reload the database session
        """
        try:
            # Create metadata
            Base.metadata.create_all(self.__engine)
            # Create a new session
            self.__session = scoped_session(sessionmaker(
                bind=self.__engine, expire_on_commit=True))
        except Exception as e:
            # Handle any errors that occur during
            # metadata creation or session initialization
            print(f"Error occurred during reload: {e}")

    def close(self):
        """
        Call close() method
        Closes the current database session
        """
        self.__session.close()
