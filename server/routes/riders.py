from flask import Blueprint, request, current_app
from utils.response import success_response, error_response
from utils.auth_helpers import token_required
import json
import os

riders_bp = Blueprint('riders', __name__)

# 临时数据，在实际环境中应该从数据库获取
RIDERS_DATA = {
    "rider_1": {
        "id": "rider_1",
        "name": "送餐员喜多郁代",
        "avatar": "/images/avatar1.jpg",
        "stats": {
            "onTimeRate": 0.98,
            "positiveFeedbackRate": 0.95,
            "averageDailyOrders": 35,
            "likeCount": 1250,
            "reviewKeywords": [
                {"text": "速度快", "weight": 5, "sentiment": "positive"},
                {"text": "态度好", "weight": 4, "sentiment": "positive"},
                {"text": "准时", "weight": 4, "sentiment": "positive"},
                {"text": "专业", "weight": 3, "sentiment": "positive"},
                {"text": "餐品完好", "weight": 3, "sentiment": "positive"},
                {"text": "礼貌", "weight": 2, "sentiment": "positive"},
                {"text": "高效", "weight": 3, "sentiment": "positive"},
                {"text": "有点慢", "weight": 2, "sentiment": "negative"},
                {"text": "包装洒了", "weight": 1, "sentiment": "negative"}
            ]
        }
    },
    "rider_2": {
        "id": "rider_2",
        "name": "送餐员波奇",
        "avatar": "/images/avatar2.jpg",
        "stats": {
            "onTimeRate": 0.92,
            "positiveFeedbackRate": 0.88,
            "averageDailyOrders": 28,
            "likeCount": 890,
            "reviewKeywords": [
                {"text": "细心", "weight": 4, "sentiment": "positive"},
                {"text": "安静", "weight": 3, "sentiment": "neutral"},
                {"text": "略慢", "weight": 3, "sentiment": "negative"},
                {"text": "餐品保温好", "weight": 4, "sentiment": "positive"},
                {"text": "路线不熟", "weight": 2, "sentiment": "negative"}
            ]
        }
    },
    "rider_3": {
        "id": "rider_3",
        "name": "送餐员凉",
        "avatar": "/images/avatar3.jpg",
        "stats": {
            "onTimeRate": 0.95,
            "positiveFeedbackRate": 0.92,
            "averageDailyOrders": 30,
            "likeCount": 1050,
            "reviewKeywords": [
                {"text": "冷静", "weight": 3, "sentiment": "neutral"},
                {"text": "效率高", "weight": 4, "sentiment": "positive"},
                {"text": "话不多", "weight": 2, "sentiment": "neutral"},
                {"text": "找零快", "weight": 3, "sentiment": "positive"}
            ]
        }
    },
    "rider_4": {
        "id": "rider_4",
        "name": "送餐员虹夏",
        "avatar": "/images/avatar4.jpg",
        "stats": {
            "onTimeRate": 0.99,
            "positiveFeedbackRate": 0.97,
            "averageDailyOrders": 40,
            "likeCount": 1500,
            "reviewKeywords": [
                {"text": "非常准时", "weight": 5, "sentiment": "positive"},
                {"text": "亲切", "weight": 4, "sentiment": "positive"},
                {"text": "可靠", "weight": 5, "sentiment": "positive"},
                {"text": "沟通顺畅", "weight": 3, "sentiment": "positive"},
                {"text": "笑容好", "weight": 3, "sentiment": "positive"}
            ]
        }
    }
}

ORDERS_DATA = {
    "user_abc": {
        "rider_1": [
            {
                "orderId": "order_1001",
                "date": "2023-10-25T12:30:00Z",
                "restaurantName": "美味快餐店",
                "items": ["香辣鸡腿堡套餐", "可乐"],
                "totalAmount": 35.50,
                "userReview": {
                    "rating": 5,
                    "comment": "送餐非常快，态度也很好！"
                }
            },
            {
                "orderId": "order_1005",
                "date": "2023-10-27T18:00:00Z",
                "restaurantName": "健康沙拉吧",
                "items": ["鸡胸肉沙拉", "鲜榨橙汁"],
                "totalAmount": 42.00,
                "userReview": None
            }
        ],
        "rider_2": [
            {
                "orderId": "order_1002",
                "date": "2023-10-26T19:15:00Z",
                "restaurantName": "深夜食堂",
                "items": ["日式拉面"],
                "totalAmount": 28.00,
                "userReview": {
                    "rating": 4,
                    "comment": "稍微晚了一点点，但态度不错。"
                }
            }
        ]
    }
}

@riders_bp.route('/list', methods=['POST', 'OPTIONS'])
@token_required
def get_riders_list(current_user):
    """获取骑手列表"""
    try:
        riders_list = list(RIDERS_DATA.values())
        return success_response(riders_list)
    except Exception as e:
        current_app.logger.error(f"获取骑手列表失败: {str(e)}")
        return error_response(f"获取骑手列表失败: {str(e)}")

@riders_bp.route('/<rider_id>', methods=['POST', 'OPTIONS'])
@token_required
def get_rider_details(current_user, rider_id):
    """获取特定骑手的详细信息"""
    try:
        if rider_id not in RIDERS_DATA:
            return error_response("骑手不存在", 404)
        
        rider_data = RIDERS_DATA[rider_id]
        return success_response(rider_data)
    except Exception as e:
        current_app.logger.error(f"获取骑手详情失败: {str(e)}")
        return error_response(f"获取骑手详情失败: {str(e)}")

@riders_bp.route('/<rider_id>/orders', methods=['POST', 'OPTIONS'])
@token_required
def get_rider_order_history(current_user, rider_id):
    """获取当前用户与特定骑手的历史订单"""
    try:
        # 这里应该根据当前用户ID获取数据，暂时使用固定用户
        user_id = "user_abc"  # 在实际环境中应该使用 current_user.username 或其他标识
        
        if user_id not in ORDERS_DATA:
            return success_response([])
        
        if rider_id not in ORDERS_DATA[user_id]:
            return success_response([])
        
        orders = ORDERS_DATA[user_id][rider_id]
        return success_response(orders)
    except Exception as e:
        current_app.logger.error(f"获取骑手订单历史失败: {str(e)}")
        return error_response(f"获取骑手订单历史失败: {str(e)}")

@riders_bp.route('/<rider_id>/like', methods=['POST', 'OPTIONS'])
@token_required
def like_rider(current_user, rider_id):
    """点赞骑手"""
    try:
        data = request.get_json()
        is_liked = data.get('isLiked', False)
        
        if rider_id not in RIDERS_DATA:
            return error_response("骑手不存在", 404)
        
        # 在实际环境中，这里应该更新数据库
        # 暂时只返回成功响应
        current_likes = RIDERS_DATA[rider_id]['stats']['likeCount']
        new_likes = current_likes + 1 if is_liked else max(0, current_likes - 1)
        
        return success_response({
            'likeCount': new_likes,
            'isLiked': is_liked
        })
    except Exception as e:
        current_app.logger.error(f"点赞骑手失败: {str(e)}")
        return error_response(f"点赞骑手失败: {str(e)}")
