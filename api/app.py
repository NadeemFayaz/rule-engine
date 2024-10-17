# api/app.py
from flask import Flask, request, jsonify
from backend.rule_engine import create_rule, combine_rules, evaluate_rule
from backend.database import save_rule, get_rule

app = Flask(__name__)

@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    rule_string = request.json.get("rule")
    rule_ast = create_rule(rule_string)
    rule_id = save_rule(rule_ast, {"author": "admin"})
    return jsonify({"rule_id": str(rule_id), "ast": rule_ast.__dict__})

@app.route('/combine_rules', methods=['POST'])
def combine_rules_api():
    rules = request.json.get("rules")
    combined_ast = combine_rules(rules)
    return jsonify({"combined_ast": combined_ast.__dict__})

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_api():
    rule_id = request.json.get("rule_id")
    data = request.json.get("data")
    rule = get_rule(rule_id)
    ast = rule['ast']
    result = evaluate_rule(Node(**ast), data)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
