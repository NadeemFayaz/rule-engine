from pymongo import MongoClient

# Initialize the MongoDB client and database
client = MongoClient('mongodb://localhost:27017/')  # Update the URI as needed
db = client['rule_engine_db']
rules_collection = db['rules']

def save_rule(rule_ast, metadata):
    try:
        rule_id = rules_collection.insert_one({
            "rule_ast": rule_ast,  # This is now a JSON-serializable dictionary
            "metadata": metadata
        }).inserted_id
        print(f"Inserted rule with ID: {rule_id}")
        return rule_id
    except Exception as e:
        print(f"Error saving rule to database: {e}")
        raise  # Re-raise the exception to be handled in the route


def get_rule(rule_id):
    return rules_collection.find_one({"_id": rule_id})
