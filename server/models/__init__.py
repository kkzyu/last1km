from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 导入所有模型类
from .user import User
from .deliverer import Deliverer
from .order import Order
from .address import Address
from .chat_message import ChatMessage

# 确保所有模型都被导出
__all__ = ['db', 'User', 'Deliverer', 'Order', 'Address', 'ChatMessage']
