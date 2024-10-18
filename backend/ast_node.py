class Node:
    def __init__(self, node_type, value, left=None, right=None):
        self.node_type = node_type
        self.value = value
        self.left = left  # Left child for binary operations
        self.right = right  # Right child for binary operations
    
    def to_dict(self):
        node_dict = {
            "node_type": self.node_type,
            "value": self.value
        }
        if self.left:
            node_dict["left"] = self.left.to_dict()  # Recursively convert left child to dict
        if self.right:
            node_dict["right"] = self.right.to_dict()  # Recursively convert right child to dict
        return node_dict
