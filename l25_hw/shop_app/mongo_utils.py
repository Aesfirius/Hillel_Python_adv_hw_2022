import os
import pymongo
import motor.motor_tornado
from asgiref.sync import sync_to_async

"""

"""


class DB:
    def __init__(self):
        self.login = os.environ.get('DB_USERNAME')
        self.password = os.environ.get('DB_PASSWORD')
        self.hostname = os.environ.get('DB_HOSTNAME')
        self.port = os.environ.get('DB_PORT')
        self.db_name = os.environ.get('DB_NAME')
        self.client = pymongo.MongoClient(f"mongodb://{self.login}:{self.password}@{self.hostname}:{self.port}")
        # self.client = motor.motor_tornado.MotorClient(f"mongodb://{self.login}:{self.password}@{self.hostname}:{self.port}")
        self.db = self.client[self.db_name]

    def get_data(self, data, collection_name):
        collection = self.db[collection_name]
        resp = collection.find_one(data)
        self.client.close()
        return resp

    @sync_to_async
    def get_all(self, data=None, collection_name=None):
        collection = self.db[collection_name]
        if data is not None:
            resp = list(collection.find(data).sort('category_name'))
        else:
            resp = list(collection.find().sort('category_name'))
        self.client.close()
        return resp

    def write_data(self, data, collection_name):
        collection = self.db[collection_name]
        collection.insert_one(data)
        self.client.close()
