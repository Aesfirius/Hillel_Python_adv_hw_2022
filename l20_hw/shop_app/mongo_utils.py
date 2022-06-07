"""
docker network create mongo-net

docker run -d --name mongodb_shop -p 27017:27017 -v ~/mongodata:/data/db -e MONGO_INITDB_ROOT_USERNAME='docker' -e MONGO_INITDB_DATABASE='db' -e MONGO_INITDB_ROOT_PASSWORD='mongopw' --hostname mongodb_shop --network mongo-net mongo

docker run -d --name mongo-express -p 8081:8081 -e ME_CONFIG_MONGODB_ADMINUSERNAME='docker' -e ME_CONFIG_MONGODB_ADMINPASSWORD='mongopw' -e ME_CONFIG_MONGODB_SERVER='mongodb_shop' -e ME_CONFIG_MONGODB_PORT=27017 --hostname mongo-express --network mongo-net mongo-express

mongodb://docker:mongopw@localhost:27017

"""
import os
import pymongo
from contextlib import ContextDecorator


# class connect_db(ContextDecorator):
#     def __int__(self):
#         self.client = pymongo.MongoClient("mongodb://docker:mongopw@localhost:27017")
#         self.db = self.client['db']
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, *exc):
#         return self.client.close()


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


# def init_db():
#     client = pymongo.MongoClient("mongodb://docker:mongopw@localhost:49153")
#     db = client['db']
#     return db, client

@connect_db()
def get_data(self, data, collection_name):
    collection = self.db[collection_name]
    resp = collection.find_one(data)
    return resp


@connect_db()
def write_data(data, collection_name):
    with connect_db() as db:
        collection = db[collection_name]
        collection.insert_one(data)
