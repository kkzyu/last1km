from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.order import Order
from models.user import User
from datetime import datetime
from models.deliverer import Deliverer
from utils.response import success_response, error_response
import os
from werkzeug.utils import secure_filename

orders_bp = Blueprint('orders', __name__)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@orders_bp.route('/my-orders', methods=['GET'])
@jwt_required()
def get_my_orders():
    """获取当前用户的所有订单"""
    try:
        current_user_id = get_jwt_identity()
        
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', None)  # 可选的状态过滤
        
        # 构建查询
        query = Order.query.filter_by(user_id=current_user_id)
        
        if status:
            query = query.filter_by(order_status=status)
            
        # 按创建时间倒序排列
        query = query.order_by(Order.created_at.desc())
        
        # 分页
        orders = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return success_response({
            'orders': [order.to_dict() for order in orders.items],
            'total': orders.total,
            'pages': orders.pages,
            'current_page': page,
            'has_next': orders.has_next,
            'has_prev': orders.has_prev
        }, "获取订单列表成功")
        
    except Exception as e:
        return error_response(f"获取订单失败: {str(e)}", 500)

@orders_bp.route('/create', methods=['POST'])
@jwt_required()
def create_order():
    """创建新订单"""
    try:
        current_user_id = get_jwt_identity()
        
        # 获取JSON数据
        data = request.get_json()
        
        if not data:
            return error_response("请求数据不能为空", 400)
        
        # 验证必需字段
        required_fields = ['start_address', 'end_address', 'total_amount', 'actual_amount']
        for field in required_fields:
            if field not in data or not data[field]:
                return error_response(f"缺少必需字段: {field}", 400)
        
        # 创建订单
        order = Order(
            user_id=current_user_id,
            start_address=data['start_address'],
            end_address=data['end_address'],
            item_description=data.get('item_description', ''),
            pickup_code=data.get('pickup_code', ''),
            locker_number=data.get('locker_number', ''),
            total_amount=float(data['total_amount']),
            coupon_discount=float(data.get('coupon_discount', 0.0)),
            actual_amount=float(data['actual_amount']),
            order_status='pending'
        )
        
        db.session.add(order)
        db.session.commit()
        
        return success_response(order.to_dict(), "订单创建成功", 201)
        
    except ValueError as e:
        return error_response("数据格式错误", 400)
    except Exception as e:
        return error_response(f"创建订单失败: {str(e)}", 500)

@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order_detail(order_id):
    """获取订单详情"""
    try:
        current_user_id = get_jwt_identity()
        
        order = Order.query.filter_by(id=order_id, user_id=current_user_id).first()
        
        if not order:
            return error_response("订单不存在", 404)
        
        return success_response(order.to_dict(), "获取订单详情成功")
        
    except Exception as e:
        return error_response(f"获取订单详情失败: {str(e)}", 500)

@orders_bp.route('/<int:order_id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_order(order_id):
    """取消订单"""
    try:
        current_user_id = get_jwt_identity()
        
        order = Order.query.filter_by(id=order_id, user_id=current_user_id).first()
        
        if not order:
            return error_response("订单不存在", 404)
        
        if order.order_status not in ['pending']:
            return error_response("只能取消待接单的订单", 400)
        
        order.order_status = 'cancelled'
        order.cancelled_at = db.func.now()
        
        db.session.commit()
        
        return success_response(order.to_dict(), "订单取消成功")
        
    except Exception as e:
        return error_response(f"取消订单失败: {str(e)}", 500)

@orders_bp.route('/<int:order_id>/restore', methods=['PUT'])
@jwt_required()
def restore_order(order_id):
    """恢复已取消的订单"""
    try:
        current_user_id = get_jwt_identity()
        
        order = Order.query.filter_by(id=order_id, user_id=current_user_id).first()
        
        if not order:
            return error_response("订单不存在", 404)
        
        if order.order_status != 'cancelled':
            return error_response("只能恢复已取消的订单", 400)
        
        order.order_status = 'pending'
        order.cancelled_at = None
        
        db.session.commit()
        
        return success_response(order.to_dict(), "订单恢复成功")
        
    except Exception as e:
        return error_response(f"恢复订单失败: {str(e)}", 500)

@orders_bp.route('/upload-image', methods=['POST'])
@jwt_required()
def upload_order_image():
    """上传订单截图"""
    try:
        if 'file' not in request.files:
            return error_response("没有文件上传", 400)
        
        file = request.files['file']
        
        if file.filename == '':
            return error_response("没有选择文件", 400)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 添加时间戳避免文件名冲突
            import time
            timestamp = str(int(time.time()))
            filename = f"{timestamp}_{filename}"
            
            # 确保上传目录存在
            upload_dir = 'uploads/order_images'
            os.makedirs(upload_dir, exist_ok=True)
            
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)
            
            return success_response({
                'filename': filename,
                'file_path': file_path,
                'url': f"/uploads/order_images/{filename}"
            }, "图片上传成功")
        else:
            return error_response("不支持的文件格式", 400)
            
    except Exception as e:
        return error_response(f"上传失败: {str(e)}", 500)

@orders_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_order_statistics():
    """获取用户订单统计"""
    try:
        current_user_id = get_jwt_identity()
        
        # 统计各状态订单数量
        total_orders = Order.query.filter_by(user_id=current_user_id).count()
        pending_orders = Order.query.filter_by(user_id=current_user_id, order_status='pending').count()
        accepted_orders = Order.query.filter_by(user_id=current_user_id, order_status='accepted').count()
        delivering_orders = Order.query.filter_by(user_id=current_user_id, order_status='delivering').count()
        completed_orders = Order.query.filter_by(user_id=current_user_id, order_status='completed').count()
        cancelled_orders = Order.query.filter_by(user_id=current_user_id, order_status='cancelled').count()
        
        # 计算总消费
        total_spent = db.session.query(db.func.sum(Order.actual_amount)).filter_by(
            user_id=current_user_id, 
            order_status='completed'
        ).scalar() or 0.0
        
        statistics = {
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'accepted_orders': accepted_orders,
            'delivering_orders': delivering_orders,
            'completed_orders': completed_orders,
            'cancelled_orders': cancelled_orders,
            'total_spent': float(total_spent)
        }
        
        return success_response(statistics, "获取统计数据成功")
        
    except Exception as e:
        return error_response(f"获取统计数据失败: {str(e)}", 500)
    
# 添加下面的路由函数
@orders_bp.route('/<int:order_id>/review', methods=['POST'])
@jwt_required()
def review_order(order_id):
    """添加订单评价"""
    try:
        current_user_id = get_jwt_identity()
        
        # 检查订单是否存在且属于当前用户
        order = Order.query.filter_by(id=order_id, user_id=current_user_id).first()
        if not order:
            return error_response("订单不存在或无权评价", 404)
        
        # 检查订单状态是否允许评价
        if order.order_status != 'completed':
            return error_response("只能评价已完成的订单", 400)
        
        # 检查是否已经评价过
        if order.user_review:
            return error_response("订单已评价，不可重复评价", 400)
        
        data = request.get_json()
        if not data or 'rating' not in data:
            return error_response("评分不能为空", 400)
        
        # 验证评分范围
        rating = float(data['rating'])
        if rating < 1 or rating > 5:
            return error_response("评分必须在1-5之间", 400)
        
        # 保存评价
        order.user_rating = rating
        order.user_review = data.get('comment', '')
        order.review_time = datetime.utcnow()
        
        # 如果有配送员，更新配送员评分
        if order.deliverer_id:
            # 获取配送员的所有评价
            deliverer_ratings = Order.query.filter_by(
                deliverer_id=order.deliverer_id,
                order_status='completed'
            ).with_entities(Order.user_rating).filter(Order.user_rating != None).all()
            
            # 计算新的平均评分
            rating_values = [r[0] for r in deliverer_ratings if r[0] is not None]
            if rating_values:
                new_avg_rating = sum(rating_values) / len(rating_values)
                
                # 更新配送员评分
                deliverer = Deliverer.query.get(order.deliverer_id)
                if deliverer:
                    deliverer.rating = new_avg_rating
        
        db.session.commit()
        
        return success_response({"order_id": order_id, "rating": rating}, "评价成功")
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"评价失败: {str(e)}", 500)