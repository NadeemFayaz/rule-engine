# backend/database.py
import pymongo
from bson import ObjectId

# Setup MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["rule_engine"]

# Collection for storing rules
rules_collection = db["rules"]

def save_rule(rule_ast, metadata):
    rule_id = rules_collection.insert_one({
        "ast": rule_ast.__dict__,
        "metadata": metadata
    }).inserted_id
    return rule_id

def get_rule(rule_id):
    rule = rules_collection.find_one({"_id": ObjectId(rule_id)})
    return rule
