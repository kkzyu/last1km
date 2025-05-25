from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.user import User
from models.order import Order
from models.address import Address
from utils.response import success_response, error_response
from utils.auth_helpers import token_required

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['POST'])
@token_required
def create_order(current_user):
    """创建订单"""
    try:
        data = request.get_json()
        start_address = data.get('start_address')
        end_address = data.get('end_address')
        item_description = data.get('item_description')
        total_amount = data.get('total_amount')
        
        if not all([start_address, end_address, total_amount]):
            return error_response("订单信息不完整")
        
        order = Order(
            user_id=current_user.id,
            start_address=start_address,
            end_address=end_address,
            item_description=item_description,
            total_amount=total_amount,
            actual_amount=total_amount
        )
        
        db.session.add(order)
        db.session.commit()
        
        return success_response(order.to_dict(), "订单创建成功")
        
    except Exception as e:
        return error_response(f"订单创建失败: {str(e)}")

@orders_bp.route('/', methods=['GET'])
@token_required
def get_orders(current_user):
    """获取订单列表"""
    try:
        orders = Order.query.filter_by(user_id=current_user.id).all()
        return success_response([order.to_dict() for order in orders])
        
    except Exception as e:
        return error_response(f"获取订单列表失败: {str(e)}")

@orders_bp.route('/<int:order_id>', methods=['GET'])
@token_required
def get_order(current_user, order_id):
    """获取订单详情"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return error_response("订单不存在", 404)
            
        if order.user_id != current_user.id:
            return error_response("无权访问该订单", 403)
            
        return success_response(order.to_dict())
        
    except Exception as e:
        return error_response(f"获取订单详情失败: {str(e)}")

@orders_bp.route('/<int:order_id>/cancel', methods=['POST'])
@token_required
def cancel_order(current_user, order_id):
    """取消订单"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return error_response("订单不存在", 404)
            
        if order.user_id != current_user.id:
            return error_response("无权取消该订单", 403)
            
        if order.order_status != 'pending':
            return error_response("只能取消待接单的订单")
            
        order.order_status = 'cancelled'
        order.cancelled_at = datetime.utcnow()
        db.session.commit()
        
        return success_response(message="订单已取消")
        
    except Exception as e:
        return error_response(f"取消订单失败: {str(e)}")
