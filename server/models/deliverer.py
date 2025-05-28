from models import db
from datetime import datetime

class Deliverer(db.Model):
    __tablename__ = 'deliverers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Float, default=5.0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系定义 - 在这边定义 backref
    orders = db.relationship('Order', backref='deliverer', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'rating': self.rating,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }