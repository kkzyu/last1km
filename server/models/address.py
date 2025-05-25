from . import db
from datetime import datetime

class Address(db.Model):
    __tablename__ = 'addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    address_type = db.Column(db.String(20), nullable=False)  # 'start' or 'end'
    address_name = db.Column(db.String(100), nullable=False)
    detailed_address = db.Column(db.Text, nullable=False)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'address_type': self.address_type,
            'address_name': self.address_name,
            'detailed_address': self.detailed_address,
            'is_default': self.is_default,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
