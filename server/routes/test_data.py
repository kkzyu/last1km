# 创建新文件用于生成测试数据

from flask import Blueprint, jsonify
from models import db, User, Order
from datetime import datetime, timedelta
import random

test_data_bp = Blueprint('test_data', __name__)

@test_data_bp.route('/create-test-orders', methods=['POST'])
def create_test_orders():
    """为当前用户创建测试订单数据"""
    try:
        # 假设有一个测试用户ID为1，或者从JWT获取当前用户
        user_id = 1  # 或使用 get_jwt_identity()
        
        # 检查用户是否存在
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "用户不存在"}), 404
        
        # 删除该用户的现有测试订单
        Order.query.filter_by(user_id=user_id).delete()
        
        # 创建测试订单数据
        test_orders_data = [
            {
                "start_address": "浙江大学紫金港校区东1舍",
                "end_address": "浙江大学紫金港校区西门外卖柜",
                "item_description": "麦当劳巨无霸套餐",
                "total_amount": 15.0,
                "actual_amount": 15.0,
                "order_status": "completed",
                "created_at": datetime.now() - timedelta(days=3),
                "pickup_code": "1234",
                "locker_number": "A01"
            },
            {
                "start_address": "浙江大学紫金港校区东2舍",
                "end_address": "浙江大学紫金港校区南门外卖柜",
                "item_description": "肯德基全家桶",
                "total_amount": 12.0,
                "actual_amount": 12.0,
                "order_status": "delivering",
                "created_at": datetime.now() - timedelta(hours=2),
                "pickup_code": "5678",
                "locker_number": "B05"
            },
            {
                "start_address": "浙江大学紫金港校区东3舍",
                "end_address": "浙江大学紫金港校区北门外卖柜",
                "item_description": "星巴克咖啡",
                "total_amount": 8.0,
                "actual_amount": 8.0,
                "order_status": "pending",
                "created_at": datetime.now() - timedelta(minutes=30),
                "pickup_code": "9999",
                "locker_number": "C10"
            },
            {
                "start_address": "浙江大学紫金港校区东4舍",
                "end_address": "浙江大学紫金港校区东门外卖柜",
                "item_description": "海底捞火锅",
                "total_amount": 25.0,
                "actual_amount": 20.0,
                "coupon_discount": 5.0,
                "order_status": "cancelled",
                "created_at": datetime.now() - timedelta(days=1),
                "cancelled_at": datetime.now() - timedelta(hours=20),
                "pickup_code": "7777",
                "locker_number": "D15"
            }
        ]
        
        # 插入测试订单
        for order_data in test_orders_data:
            order = Order(
                user_id=user_id,
                **order_data
            )
            db.session.add(order)
        
        db.session.commit()
        
        return jsonify({
            "message": f"成功创建 {len(test_orders_data)} 个测试订单",
            "user_id": user_id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"创建测试数据失败: {str(e)}"}), 500