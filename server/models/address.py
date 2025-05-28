from models import db
from datetime import datetime

class Address(db.Model):
    __tablename__ = 'addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    address_type = db.Column(db.String(20), nullable=False)  # pickup, delivery
    name = db.Column(db.String(100), nullable=False)  # 地址名称
    address_detail = db.Column(db.String(500), nullable=False)  # 详细地址
    contact_person = db.Column(db.String(50))  # 联系人
    contact_phone = db.Column(db.String(20))  # 联系电话
    notes = db.Column(db.String(200))  # 备注
    is_default = db.Column(db.Boolean, default=False)  # 是否为默认地址
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Address {self.name}: {self.address_detail}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'address_type': self.address_type,
            'name': self.name,
            'address_detail': self.address_detail,
            'contact_person': self.contact_person,
            'contact_phone': self.contact_phone,
            'notes': self.notes,
            'is_default': self.is_default,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }