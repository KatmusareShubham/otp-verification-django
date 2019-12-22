from pymongo import MongoClient

def connect_db(database_name):
    client = MongoClient('localhost', 27018)
    db = client[database_name]
    return db


