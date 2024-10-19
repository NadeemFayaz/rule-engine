class Node:
    def __init__(self, node_type, value, left=None, right=None):
        self.node_type = node_type
        self.value = value
        self.left = left
        self.right = right

    def to_dict(self):
        return {
            'node_type': self.node_type,
            'value': self.value,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None
        }

    @staticmethod
    def from_dict(data):
        if not data:
            return None
        return Node(
            node_type=data['node_type'],
            value=data['value'],
            left=Node.from_dict(data.get('left')),
            right=Node.from_dict(data.get('right'))
        )
