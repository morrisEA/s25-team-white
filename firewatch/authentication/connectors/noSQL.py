from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
from .base_connector import BaseDatabaseConnector

import os

class NoSQLDatabaseConnector(BaseDatabaseConnector):
    """MongoDB Connector for Military Personnel & Firearm Transactions"""

    def __init__(self, mongo_uri=None):
        """Initialize MongoDB connection"""
        self.client = MongoClient(mongo_uri or os.getenv("MONGO_URI", "mongodb://localhost:27017/firewatch"))
        self.db = self.client.get_database("firewatch")

    def save_personnel(self, personnel_data):
        """Saves military personnel with hashed password"""
        personnel_data["password"] = generate_password_hash(personnel_data["password"])
        self.db.personnel.insert_one(personnel_data)

    def authenticate_personnel(self, username, password):
        """Authenticate user from MongoDB"""
        personnel = self.db.personnel.find_one({"username": username})
        return personnel and check_password_hash(personnel["password"], password)

    def save_firearm(self, firearm_data):
        """Saves firearm data in MongoDB"""
        self.db.firearms.insert_one(firearm_data)

    def check_out_firearm(self, firearm_id, personnel_id):
        """Handles firearm check-out in MongoDB"""
        self.db.transactions.insert_one({
            "firearm_id": firearm_id,
            "personnel_id": personnel_id,
            "status": "OUT"
        })
