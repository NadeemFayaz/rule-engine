from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
from backend.ast_node import Node  # Replace 'backend.ast_node' with the correct module
from backend.rule_engine import create_rule, combine_rules, evaluate_rule
from backend.database import save_rule, get_rule
import logging
from bson import ObjectId  # Import ObjectId if not already imported

# logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

# Define the root route
@app.route('/')
def home():
    return jsonify(message="Welcome to the Rule Engine API!")

# Route for creating a rule

# Route to create a rule
@app.route('/create_rule', methods=['POST'])
def create_rule_route():
    data = request.json
    rule_string = data.get('rule_string')

    if rule_string:
        try:
            # Create the AST for the rule
            rule_ast = create_rule(rule_string)
            app.logger.debug(f"Rule AST: {rule_ast}")

            # Convert the AST Node object to a serializable dictionary
            rule_dict = rule_ast.to_dict()  # Assuming to_dict() converts AST to dictionary

            # Save rule to the database
            rule_id = save_rule(rule_dict, {"rule_string": rule_string})  # Save both rule_string and AST
            return jsonify(rule_id=str(rule_id)), 201  # Return the rule ID
        except Exception as e:
            app.logger.error(f"Error creating rule: {str(e)}")  # Log the error
            return jsonify(error=f"Error creating rule: {str(e)}"), 500  # Return detailed error message
    else:
        app.logger.error("Missing 'rule_string' in request data.")
        return jsonify(error="Missing 'rule_string' in request data."), 400


# Route for combining rules


@app.route('/combine_rules', methods=['POST'])
def combine_rules_route():
    data = request.json  # Expecting JSON data with a list of rules
    app.logger.debug(f"Received data: {data}")

    rule_strings = data.get('rule_strings')
    if not rule_strings or not isinstance(rule_strings, list):
        app.logger.error("Missing or invalid 'rule_strings' in request data.")
        return jsonify(error="Missing or invalid rule_strings"), 400  # Bad request

    try:
        combined_ast = combine_rules(rule_strings)  # Combine the rules into a single AST
        app.logger.debug(f"Combined Rule AST: {combined_ast}")
        return jsonify(ast=combined_ast.to_dict()), 200  # Convert Node object to dict and return as JSON
    except Exception as e:
        app.logger.error(f"Error combining rules: {e}")
        return jsonify(error="Failed to combine rules"), 500
# Route for evaluating a rule
@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_route():
    data = request.json
    rule_id = data.get('rule_id')
    user_data = data.get('user_data')
    
    app.logger.debug(f"Evaluating rule {rule_id} with user data: {user_data}")
    
    # Fetch rule from database
    rule = rules_collection.find_one({"_id": ObjectId(rule_id)})
    if not rule:
        app.logger.error("Rule not found")
        return jsonify({"error": "Rule not found"}), 404
    
    # Evaluate rule
    try:
        is_eligible = evaluate_rule(rule['rule_ast'], user_data)
        app.logger.debug(f"Evaluation result: {is_eligible}")
        return jsonify({"is_eligible": is_eligible})
    except Exception as e:
        app.logger.error(f"Error evaluating rule: {e}")
        return jsonify({"error": "Failed to evaluate rule"}), 500


if __name__ == '__main__':
    app.run(debug=True)
