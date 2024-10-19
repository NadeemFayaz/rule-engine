# backend/rule_engine.py
from .ast_node import Node

def create_rule(rule_string):
    # Create an AST Node and return the Node object
    node = Node(node_type="operand", value=rule_string)
    return node  # Return the Node object itself



    

def combine_rules(rules):
    combined_ast = None
    for rule_string in rules:
        rule_ast = create_rule(rule_string)
        if not combined_ast:
            combined_ast = rule_ast
        else:
            combined_ast = Node(node_type="operator", value="AND", left=combined_ast, right=rule_ast)
    
    return combined_ast

def evaluate_rule(rule_ast, user_data):
    """
    Evaluate the given rule AST against user data.

    Parameters:
        rule_ast (dict): The AST representing the rule.
        user_data (dict): The user data to evaluate against.

    Returns:
        bool: The result of the rule evaluation.
    """
    try:
        result = evaluate_node(rule_ast, user_data)
        return {"is_eligible": result}  # Wrap the result in a response dictionary
    except Exception as e:
        return {"error": f"Error during evaluation: {str(e)}"}

def evaluate_node(node, user_data):
    """
    Recursively evaluate the AST nodes.

    Parameters:
        node (dict): The current AST node.
        user_data (dict): The user data to evaluate against.

    Returns:
        bool: The result of the evaluation for this node.
    """
    if node['node_type'] == 'operand':
        # Parse the operand expression (e.g., "age > 30")
        key, operator, threshold = parse_operand(node['value'])
        user_value = user_data.get(key)

        if user_value is None:
            raise ValueError(f"User data does not contain '{key}'")

        return apply_operator(user_value, operator, threshold)

    elif node['node_type'] == 'operator':
        left_result = evaluate_node(node['left'], user_data)
        right_result = evaluate_node(node['right'], user_data)

        if node['value'] == 'AND':
            return left_result and right_result
        elif node['value'] == 'OR':
            return left_result or right_result
        else:
            raise ValueError(f"Unknown operator '{node['value']}'")

    else:
        raise ValueError(f"Unknown node type '{node['node_type']}'")

def apply_operator(user_value, operator, threshold):
    if operator == '>':
        return user_value > threshold
    elif operator == '<':
        return user_value < threshold
    elif operator == '==':
        return user_value == threshold
    elif operator == '!=':
        return user_value != threshold
    # Add more operators as needed
    else:
        raise ValueError(f"Unknown operator '{operator}'")

def parse_operand(operand):
    # This is a simple approach; you may want to use regex for complex cases.
    parts = operand.split()
    if len(parts) != 3:
        raise ValueError("Invalid operand format.")
    
    key = parts[0]
    operator = parts[1]
    threshold = parts[2]

    # Attempt to convert the threshold to an appropriate type
    try:
        threshold = int(threshold)
    except ValueError:
        try:
            threshold = float(threshold)
        except ValueError:
            pass  # Keep as string if not a number

    return key, operator, threshold




