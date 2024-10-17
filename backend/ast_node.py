class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type  # Use `node_type` to avoid conflict
        self.left = left
        self.right = right
        self.value = value

    def to_dict(self):
        """Convert the Node to a dictionary format."""
        node_dict = {
            'node_type': self.node_type,
            'value': self.value,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None
        }
        return node_dict
