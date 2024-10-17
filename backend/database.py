# backend/database.py
import pymongo
from bson import ObjectId

# Connect to the local MongoDB instance
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Use the 'rule_engine' database
db = client["rule_engine"]

# Create or access the 'rules' collection
rules_collection = db["rules"]

def save_rule(rule_ast, metadata):
    # Convert the AST Node to a dictionary
    rule_dict = rule_ast.to_dict()
    rule_id = rules_collection.insert_one({
        'rule': rule_dict,
        'metadata': metadata
    }).inserted_id
    return rule_id


def get_rule(rule_id):
    rule = rules_collection.find_one({"_id": ObjectId(rule_id)})
    return rule
