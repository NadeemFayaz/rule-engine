from flask import Flask, jsonify, request
from backend.rule_engine import create_rule, combine_rules, evaluate_rule
from backend.database import save_rule, get_rule
import logging
from bson import ObjectId  # Import ObjectId if not already imported

# logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Define the root route
@app.route('/')
def home():
    return jsonify(message="Welcome to the Rule Engine API!")

# Route for creating a rule

@app.route('/create_rule', methods=['POST'])
def create_rule_route():
    data = request.json  # Expecting JSON data
    app.logger.debug(f"Received data: {data}")
    rule_string = data.get('rule_string')
    if not rule_string:
        app.logger.error("Missing 'rule_string' in request data.")
        return jsonify(error="Missing rule_string"), 400  # Bad request

    try:
        with open('rule.log', 'a') as f:
            f.write(f"Rule created: {rule_string}\n")

        rule_ast = create_rule(rule_string)  # Convert the rule string to an AST   
        app.logger.debug(f"Rule AST: {rule_ast}")
        
        rule_id = save_rule(rule_ast, {"rule_string": rule_string})  # Save the rule to the database
        app.logger.debug(f"Rule saved with ID: {rule_id}")
        
        # Convert ObjectId to string before returning
        return jsonify(rule_id=str(rule_id)), 201  # Return the created rule ID
    except Exception as e:
        app.logger.error(f"Error creating rule: {e}")  # Log the error
        with open('error.log', 'a') as f:
            f.write(f"Error creating rule: {e}\n")

        return jsonify(error="Failed to create rule"), 500  # Internal server error

# Route for combining rules


@app.route('/combine_rules', methods=['POST'])
def combine_rules_route():
    """
    This route takes a list of rule strings from the request and returns the combined AST.
    """
    data = request.json  # Expecting JSON data with a list of rules
    app.logger.debug(f"Received data: {data}")
    
    rule_strings = data.get('rule_strings')  # Get the list of rule strings
    if not rule_strings or not isinstance(rule_strings, list):
        app.logger.error("Missing or invalid 'rule_strings' in request data.")
        return jsonify(error="Missing or invalid rule_strings"), 400  # Bad request

    try:
        combined_ast = combine_rules(rule_strings)  # Combine the rules into a single AST
        app.logger.debug(f"Combined Rule AST: {combined_ast}")
        return jsonify(ast=combined_ast.to_dict()), 200  # Return the AST as a JSON response
    except Exception as e:
        app.logger.error(f"Error combining rules: {e}")  # Log the error
        return jsonify(error="Failed to combine rules"), 500  # Internal server error

def parse_rule_to_ast(rule_string):
    """
    Convert a single rule string (e.g., 'age > 30') into an AST node.
    """
    return Node(node_type="operand", value=rule_string)

def combine_rules(rules):
    """
    Combines a list of rule strings into a single AST.
    """
    if not rules:
        raise ValueError("No rules to combine")
    
    # Parse all rule strings into ASTs
    asts = [parse_rule_to_ast(rule) for rule in rules]
    
    # Use 'AND' to combine all ASTs, minimizing redundant checks
    combined_ast = asts[0]  # Start with the first rule's AST
    
    for ast in asts[1:]:
        combined_ast = Node(node_type="operator", value="AND", left=combined_ast, right=ast)
    
    return combined_ast  # Return the root of the combined AST




# Route for evaluating a rule
@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_route():
    data = request.json
    rule_id = data.get('rule_id')
    user_data = data.get('user_data')
    
    if rule_id and user_data:
        rule = get_rule(rule_id)  # Retrieve the rule from the database
        if rule:
            is_eligible = evaluate_rule(rule['ast'], user_data)  # Evaluate the rule with user data
            return jsonify(is_eligible=is_eligible), 200  # Return the evaluation result
        return jsonify(error="Rule not found"), 404  # Return error if rule not found
    
    return jsonify(error="Missing rule_id or user_data"), 400  # Return error if parameters are missing

if __name__ == '__main__':
    app.run(debug=True)
