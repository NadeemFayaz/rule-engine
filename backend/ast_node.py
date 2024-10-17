class Node:
    def __init__(self, node_type, value):
        self.node_type = node_type
        self.value = value
    
    def to_dict(self):
        return {
            "node_type": self.node_type,
            "value": self.value
        }

