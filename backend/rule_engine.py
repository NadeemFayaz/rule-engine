# backend/rule_engine.py
from .ast_node import Node

def create_rule(rule_string):
    # Create an AST Node and return its dictionary representation
    node = Node(node_type="operand", value=rule_string)
    return node.to_dict()


    

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
