from . import db
from datetime import datetime
import os
import uuid

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    deliverer_id = db.Column(db.Integer, db.ForeignKey('deliverers.id'))
    start_address = db.Column(db.Text, nullable=False)
    end_address = db.Column(db.Text, nullable=False)
    order_image = db.Column(db.String(255), nullable=True)  # 修改为可空，长度255
    item_description = db.Column(db.Text)
    pickup_code = db.Column(db.String(50))
    locker_number = db.Column(db.String(50))
    total_amount = db.Column(db.Float, nullable=False)
    coupon_discount = db.Column(db.Float, default=0.0)
    actual_amount = db.Column(db.Float, nullable=False)
    order_status = db.Column(db.String(20), default='pending')  # 改为英文状态
    order_no = db.Column(db.String(32), unique=True, nullable=False, default=lambda: str(uuid.uuid4()).replace('-', ''))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)
    
    # 地理位置信息
    origin_lat = db.Column(db.Float)
    origin_lng = db.Column(db.Float)
    dest_lat = db.Column(db.Float)
    dest_lng = db.Column(db.Float)
    
    # 路线信息
    estimated_duration = db.Column(db.Integer)  # 预计时长(分钟)
    estimated_distance = db.Column(db.Float)    # 预计距离(公里)
    
    # 添加具体地址字段
    origin_detail = db.Column(db.Text)        # 起点具体地址
    destination_detail = db.Column(db.Text)   # 终点具体地址

    def to_dict(self):
        return {
            'id': self.id,
            'order_no': self.order_no,
            'user_id': self.user_id,
            'deliverer_id': self.deliverer_id,
            'start_address': self.start_address,
            'end_address': self.end_address,
            'order_image': self.order_image,
            'item_description': self.item_description,
            'pickup_code': self.pickup_code,
            'locker_number': self.locker_number,
            'total_amount': self.total_amount,
            'coupon_discount': self.coupon_discount,
            'actual_amount': self.actual_amount,
            'order_status': self.order_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'accepted_at': self.accepted_at.isoformat() if self.accepted_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'cancelled_at': self.cancelled_at.isoformat() if self.cancelled_at else None,
            'origin_location': {
                'lat': self.origin_lat,
                'lng': self.origin_lng
            } if self.origin_lat and self.origin_lng else None,
            'destination_location': {
                'lat': self.dest_lat,
                'lng': self.dest_lng
            } if self.dest_lat and self.dest_lng else None,
            'estimated_duration': self.estimated_duration,
            'estimated_distance': self.estimated_distance,
            'origin_detail': self.origin_detail,
            'destination_detail': self.destination_detail,
        }
