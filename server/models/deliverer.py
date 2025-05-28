from . import db
from datetime import datetime

class Deliverer(db.Model):
    __tablename__ = 'deliverers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    rating = db.Column(db.Float, default=5.0)
    on_time_rate = db.Column(db.Float, default=100.0)
    daily_orders = db.Column(db.Integer, default=0)
    total_likes = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='online')  # online, offline
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联关系
    orders = db.relationship('Order', backref='deliverer', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'avatar': self.avatar,
            'phone': self.phone,
            'rating': self.rating,
            'on_time_rate': self.on_time_rate,
            'daily_orders': self.daily_orders,
            'total_likes': self.total_likes,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
