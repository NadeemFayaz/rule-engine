from app import db

class Rule(db.Model):
    __tablename__ = 'rules'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))  # "operator" or "operand"
    value = db.Column(db.String(255), nullable=True)  # Condition (e.g., age > 25)
    left_id = db.Column(db.Integer, db.ForeignKey('rules.id'), nullable=True)
    right_id = db.Column(db.Integer, db.ForeignKey('rules.id'), nullable=True)

    left = db.relationship('Rule', remote_side=[id], foreign_keys=[left_id], backref='left_rules')
    right = db.relationship('Rule', remote_side=[id], foreign_keys=[right_id], backref='right_rules')

    def __init__(self, type, value=None, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'value': self.value,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None
        }
