from models import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(100))
    avatar = db.Column(db.String(255))
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    balance = db.Column(db.Float, default=0.0)
    
    # 配送地址字段
    default_pickup_address = db.Column(db.Text, default='')
    default_delivery_address = db.Column(db.Text, default='')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        """更新最后登录时间"""
        self.last_login = datetime.utcnow()
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def validate_username(username):
        """验证用户名"""
        if not username or len(username.strip()) < 3:
            return False, "用户名长度不能少于3个字符"
        if len(username.strip()) > 80:
            return False, "用户名长度不能超过80个字符"
        if not re.match(r'^[a-zA-Z0-9_]+$', username.strip()):
            return False, "用户名只能包含字母、数字和下划线"
        return True, ""

    @staticmethod
    def validate_phone(phone):
        """验证手机号"""
        if not phone:
            return True, ""
        phone = phone.strip()
        if not re.match(r'^1[3-9]\d{9}$', phone):
            return False, "请输入正确的手机号格式"
        return True, ""

    @staticmethod
    def validate_email(email):
        """验证邮箱"""
        if not email:
            return True, ""
        email = email.strip()
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return False, "请输入正确的邮箱格式"
        return True, ""

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'gender': self.gender,
            'phone': self.phone,
            'email': self.email,
            'balance': self.balance,
            'default_pickup_address': self.default_pickup_address or '',
            'default_delivery_address': self.default_delivery_address or '',
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'status': self.status
        }