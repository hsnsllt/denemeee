from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["gym_system"]

        self.members = self.db["members"]
        self.subscriptions = self.db["subscriptions"]
        self.payments = self.db["payments"]

db = Database()
