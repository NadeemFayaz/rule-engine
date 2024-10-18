from pymongo import MongoClient
from bson import ObjectId

# Initialize the MongoDB client and database
client = MongoClient('mongodb://localhost:27017/')  # Update the URI as needed
db = client['rule_engine_db']
rules_collection = db['rules']

def save_rule(rule_string, rule_ast):
    try:
        # Insert the rule into the MongoDB collection
        rule_id = rules_collection.insert_one({
            "rule_string": rule_string,  # Store the original rule string
            "rule_ast": rule_ast,        # This should be a JSON-serializable dictionary
        }).inserted_id
        print(f"Inserted rule with ID: {rule_id}")
        return rule_id
    except Exception as e:
        print(f"Error saving rule to database: {e}")
        raise  # Re-raise the exception to be handled in the route

def get_rule(rule_id):
    return rules_collection.find_one({"_id": ObjectId(rule_id)})  # Convert rule_id to ObjectId
