from flask import request, jsonify
from app import app, db
from models.rule import Rule

@app.route('/rules', methods=['POST'])
def create_rule():
    data = request.get_json()

    rule_type = data['type']
    rule_value = data.get('value')
    left_rule = data.get('left')
    right_rule = data.get('right')

    # Create Rule instance
    new_rule = Rule(
        type=rule_type,
        value=rule_value,
        left=Rule.from_dict(left_rule) if left_rule else None,
        right=Rule.from_dict(right_rule) if right_rule else None
    )

    # Add and commit to database
    db.session.add(new_rule)
    db.session.commit()

    return jsonify({"message": "Rule created!", "rule": new_rule.to_dict()}), 201
