from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text
from flask_cors import CORS
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/rule_engine'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Rule(db.Model):
    id = Column(Integer, primary_key=True)
    rule_string = Column(Text, nullable=False)
    created_at = Column(db.DateTime, default=db.func.current_timestamp())

db.create_all()

@app.route('/')
def index():
    return "Rule Engine API is working!"

@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_string = request.json['rule_string']
    rule = Rule(rule_string=rule_string)
    db.session.add(rule)
    db.session.commit()
    return jsonify({'id': rule.id, 'rule_string': rule.rule_string})

@app.route('/combine_rules', methods=['POST'])
def combine_rules():
    rule_ids = request.json['rule_ids']
    rules = Rule.query.filter(Rule.id.in_(rule_ids)).all()
    combined_rule_string = ' OR '.join([rule.rule_string for rule in rules])
    combined_rule = Rule(rule_string=combined_rule_string)
    db.session.add(combined_rule)
    db.session.commit()
    return jsonify({'id': combined_rule.id, 'rule_string': combined_rule.rule_string})

@app.route('/evaluate', methods=['POST'])
def evaluate():
    rule_id = request.json['rule_id']
    data = request.json['data']
    rule = Rule.query.get(rule_id)
    ast = create_rule(rule.rule_string)
    result = evaluate_rule(ast, data)
    return jsonify({'result': result})

def create_rule(rule_string: str) -> Node:
    tokens = rule_string.split()
    stack = []
    for token in tokens:
        if token in ('AND', 'OR'):
            right = stack.pop()
            left = stack.pop()
            stack.append(Node('operator', token, left, right))
        else:
            stack.append(Node('operand', token))
    return stack[0]

def evaluate_rule(node: Node, data: dict) -> bool:
    if node.type == 'operator':
        if node.value == 'AND':
            return evaluate_rule(node.left, data) and evaluate_rule(node.right, data)
        elif node.value == 'OR':
            return evaluate_rule(node.left, data) or evaluate_rule(node.right, data)
    else:
        key, op, value = node.value.split()
        value = int(value) if value.isdigit() else value.strip("'")
        if op == '>':
            return data[key] > value
        elif op == '<':
            return data[key] < value
        elif op == '=':
            return data[key] == value
    return False

if __name__ == '__main__':
    app.run(debug=True)