from flask import Flask, jsonify, request
from backend.rule_engine import create_rule, combine_rules, evaluate_rule
from backend.database import save_rule, get_rule

app = Flask(__name__)

# Define the root route
@app.route('/')
def home():
    return jsonify(message="Welcome to the Rule Engine API!")

# Route for creating a rule
@app.route('/create_rule', methods=['POST'])
def create_rule_route():
    data = request.json  # Expecting JSON data
    rule_string = data.get('rule_string')
    if rule_string:
        rule_ast = create_rule(rule_string)  # Create the AST from the rule string
        rule_id = save_rule(rule_ast, {"rule_string": rule_string})  # Save the rule to the database
        return jsonify(rule_id=rule_id), 201  # Return the created rule ID
    return jsonify(error="Missing rule_string"), 400  # Return error if rule_string is missing

# Route for combining rules
@app.route('/combine_rules', methods=['POST'])
def combine_rules_route():
    data = request.json
    rules = data.get('rules')
    if rules:
        combined_ast = combine_rules(rules)  # Combine the provided rules into a single AST
        return jsonify(combined_ast=combined_ast), 200  # Return the combined AST
    return jsonify(error="Missing rules"), 400  # Return error if rules are missing

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
