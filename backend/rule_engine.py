# backend/rule_engine.py
from .ast_node import Node

def create_rule(rule_string):

    # For simplicity, here’s an example that directly returns an AST for rule1
    node = Node(node_type="operator", value="AND",
                left=Node(node_type="operator", value="OR",
                          left=Node(node_type="operand", value="age > 30"),
                          right=Node(node_type="operand", value="department = 'Sales'")
                         ),
                right=Node(node_type="operator", value="OR",
                           left=Node(node_type="operand", value="salary > 50000"),
                           right=Node(node_type="operand", value="experience > 5")
                          )
               )
    return node
    

def combine_rules(rules):
    combined_ast = None
    for rule_string in rules:
        rule_ast = create_rule(rule_string)
        if not combined_ast:
            combined_ast = rule_ast
        else:
            combined_ast = Node(node_type="operator", value="AND", left=combined_ast, right=rule_ast)
    
    return combined_ast

def evaluate_rule(ast, data):
    if ast.node_type == "operand":
        return eval(ast.value, {}, data)
    elif ast.node_type == "operator":
        if ast.value == "AND":
            return evaluate_rule(ast.left, data) and evaluate_rule(ast.right, data)
        elif ast.value == "OR":
            return evaluate_rule(ast.left, data) or evaluate_rule(ast.right, data)
    return False
