from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    nickname = db.Column(db.String(100))
    avatar = db.Column(db.String(200))
    gender = db.Column(db.String(10))
    school_info = db.Column(db.String(200))
    dormitory = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(20), default='active')
    
    # 关联关系
    orders = db.relationship('Order', backref='user', lazy=True)
    addresses = db.relationship('Address', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'gender': self.gender,
            'school_info': self.school_info,
            'dormitory': self.dormitory,
            'phone': self.phone,
            'balance': self.balance,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'status': self.status
        }
