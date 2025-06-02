from flask import Blueprint, jsonify
from utils.response import success_response, error_response

faq_bp = Blueprint('faq', __name__)

@faq_bp.route('/list', methods=['GET', 'OPTIONS'])
def get_faq_list():
    """获取常见问题列表"""
    try:
        # 这里可以从数据库获取，现在先使用静态数据
        faq_data = [
            {
                "id": 1,
                "question": "如何取消订单？",
                "answer": "在订单详情页面点击'取消订单'按钮即可。订单状态为'进行中'时才能取消。",
                "category": "订单管理",
                "order": 1
            },
            {
                "id": 2,
                "question": "配送费如何计算？",
                "answer": "配送费由用户自身确定，建议根据距离和时间段动态计算。若配送费过低可能导致配送员拒单。",
                "category": "费用说明",
                "order": 2
            },
            {
                "id": 3,
                "question": "如何申请退款？",
                "answer": "请联系客服或在订单页面申请退款。已完成的订单需要提供退款理由。",
                "category": "退款政策",
                "order": 3
            },
            {
                "id": 4,
                "question": "配送员联系不上怎么办？",
                "answer": "可以通过消息页面联系配送员，或者直接联系客服协助处理。",
                "category": "配送问题",
                "order": 4
            },
            {
                "id": 5,
                "question": "如何修改收货地址？",
                "answer": "在个人资料页面可以添加和修改收货地址。订单创建后地址无法修改。",
                "category": "地址管理",
                "order": 5
            },
            {
                "id": 6,
                "question": "忘记取件码怎么办？",
                "answer": "可以在订单详情页面查看取件码，或者联系配送员确认。",
                "category": "取件问题",
                "order": 6
            }
        ]
        
        return success_response(faq_data, "获取FAQ列表成功")
        
    except Exception as e:
        return error_response(f"获取FAQ列表失败: {str(e)}")

@faq_bp.route('/categories', methods=['GET', 'OPTIONS'])
def get_faq_categories():
    """获取FAQ分类列表"""
    try:
        categories = [
            {"id": 1, "name": "订单管理", "icon": "fas fa-list-alt"},
            {"id": 2, "name": "费用说明", "icon": "fas fa-money-bill-wave"},
            {"id": 3, "name": "退款政策", "icon": "fas fa-undo"},
            {"id": 4, "name": "配送问题", "icon": "fas fa-truck"},
            {"id": 5, "name": "地址管理", "icon": "fas fa-map-marker-alt"},
            {"id": 6, "name": "取件问题", "icon": "fas fa-box"}
        ]
        
        return success_response(categories, "获取FAQ分类成功")
        
    except Exception as e:
        return error_response(f"获取FAQ分类失败: {str(e)}")