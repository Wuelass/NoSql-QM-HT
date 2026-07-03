import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "finance_app")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]


def get_db():
    return db
