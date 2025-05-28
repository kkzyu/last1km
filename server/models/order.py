from models import db
from datetime import datetime
import uuid

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 地址信息
    start_address = db.Column(db.String(500), nullable=False)
    end_address = db.Column(db.String(500), nullable=False)
    
    # 订单详情
    item_description = db.Column(db.Text)  # 物品描述
    pickup_code = db.Column(db.String(100))  # 取件码
    locker_number = db.Column(db.String(100))  # 柜号
    
    # 费用相关
    total_amount = db.Column(db.Float, nullable=False)  # 委托总金额
    coupon_discount = db.Column(db.Float, default=0.0)  # 优惠券抵扣
    actual_amount = db.Column(db.Float, nullable=False)  # 实付金额
    
    # 订单状态
    order_status = db.Column(db.String(50), default='pending')  # pending, accepted, delivering, completed, cancelled
    
    # 配送员相关
    deliverer_id = db.Column(db.Integer, db.ForeignKey('deliverers.id'), nullable=True)
    
    # 图片相关
    image_url = db.Column(db.String(500))  # 订单截图URL
    
    # 评价相关
    user_rating = db.Column(db.Float)  # 用户评分 1-5
    user_review = db.Column(db.Text)  # 用户评价内容
    review_time = db.Column(db.DateTime)  # 评价时间
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cancelled_at = db.Column(db.DateTime)  # 取消时间
    
    # 关系
    user = db.relationship('User', backref='orders')
    # deliverer = db.relationship('Deliverer', backref='delivered_orders')
    
    def to_dict(self):
        from models.deliverer import Deliverer
        
        deliverer_info = None
        if self.deliverer_id:
            deliverer = Deliverer.query.get(self.deliverer_id)
            if deliverer:
                deliverer_info = {
                    'id': deliverer.id,
                    'name': deliverer.name,
                    'phone': deliverer.phone,
                    'rating': deliverer.rating
                }
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'start_address': self.start_address,
            'end_address': self.end_address,
            'item_description': self.item_description,
            'pickup_code': self.pickup_code,
            'locker_number': self.locker_number,
            'total_amount': self.total_amount,
            'coupon_discount': self.coupon_discount,
            'actual_amount': self.actual_amount,
            'order_status': self.order_status,
            'deliverer_id': self.deliverer_id,
            'image_url': self.image_url,
            'user_rating': self.user_rating,
            'user_review': self.user_review,
            'review_time': self.review_time.isoformat() if self.review_time else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'cancelled_at': self.cancelled_at.isoformat() if self.cancelled_at else None,
            'deliverer': deliverer_info
        }