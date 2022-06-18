import os
import pymongo
from contextlib import ContextDecorator
"""

"""


class connect_db(ContextDecorator):
    def __init__(self):
        self.login = os.environ.get('DB_USERNAME')
        self.password = os.environ.get('DB_PASSWORD')
        self.hostname = os.environ.get('DB_HOSTNAME')
        self.port = os.environ.get('DB_PORT')
        self.db_name = os.environ.get('DB_NAME')
        self.client = None
        self.db = None

    def __enter__(self):
        self.client = pymongo.MongoClient(f"mongodb://{self.login}:{self.password}@{self.hostname}:{self.port}")
        self.db = self.client[self.db_name]
        return self.db

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.client.close()


def get_data(data, collection_name):
    with connect_db() as db:
        collection = db[collection_name]
        resp = collection.find_one(data)
    return resp


def get_all(data=None, collection_name=None):
    with connect_db() as db:
        collection = db[collection_name]
        if data is not None:
            resp = list(collection.find(data).sort('category_name'))
        else:
            resp = list(collection.find().sort('category_name'))
    return resp


def write_data(data, collection_name):
    with connect_db() as db:
        collection = db[collection_name]
        collection.insert_one(data)
