from flask import Blueprint, request, current_app
from utils.response import success_response, error_response
from utils.auth_helpers import token_required
import json
import os
from datetime import datetime, timedelta

messages_bp = Blueprint('messages', __name__)

# 临时聊天数据，在实际环境中应该从数据库获取
CHATS_DATA = [
    {
        "id": "chat_rider_1",
        "riderId": "rider_1",
        "lastMessage": "您的外卖已经送至青溪4舍711，请及时领取~",
        "minutesAgo": 5,
        "unreadCount": 2
    },
    {
        "id": "chat_rider_2",
        "riderId": "rider_2",
        "lastMessage": "请及时领取…谢谢！",
        "minutesAgo": 120,
        "unreadCount": 3
    },
    {
        "id": "chat_rider_3",
        "riderId": "rider_3",
        "lastMessage": "711。取。",
        "minutesAgo": 30,
        "unreadCount": 1
    },
    {
        "id": "chat_rider_4",
        "riderId": "rider_4",
        "lastMessage": "您的外卖已经送至青溪4舍楼下寄存点，请及时领取~",
        "minutesAgo": 15,
        "unreadCount": 1
    }
]

RIDERS_DATA = {
    "rider_1": {
        "id": "rider_1",
        "name": "送餐员喜多郁代",
        "avatar": "/images/avatar1.jpg"
    },
    "rider_2": {
        "id": "rider_2",
        "name": "送餐员波奇",
        "avatar": "/images/avatar2.jpg"
    },
    "rider_3": {
        "id": "rider_3",
        "name": "送餐员凉",
        "avatar": "/images/avatar3.jpg"
    },
    "rider_4": {
        "id": "rider_4",
        "name": "送餐员虹夏",
        "avatar": "/images/avatar4.jpg"
    }
}

MESSAGES_DATA = {
    "chat_rider_1": {
        "rider": {
            "id": "rider_1",
            "name": "送餐员喜多郁代",
            "avatar": "/images/avatar1.jpg"
        },
        "messages": [
            {"id": "msg1", "text": "您好，您的订单已接单，正在火速赶往目的地。", "sender": "rider", "timestamp": "2023-10-26T10:00:00.000Z"},
            {"id": "msg2", "text": "好的，谢谢！", "sender": "user", "timestamp": "2023-10-26T10:01:00.000Z"},
            {"id": "msg3", "text": "您的外卖已经送至青溪4舍711，请及时领取~", "sender": "rider", "timestamp": "2023-10-26T10:05:00.000Z"}
        ]
    },
    "chat_rider_2": {
        "rider": {
            "id": "rider_2",
            "name": "送餐员波奇",
            "avatar": "/images/avatar2.jpg"
        },
        "messages": [
            {"id": "msg4", "text": "您好，外卖放到青溪4舍了。", "sender": "rider", "timestamp": "2023-10-26T08:30:00.000Z"},
            {"id": "msg5", "text": "请及时领取…谢谢！", "sender": "rider", "timestamp": "2023-10-26T08:30:00.000Z"}
        ]
    },
    "chat_rider_3": {
        "rider": {
            "id": "rider_3",
            "name": "送餐员凉",
            "avatar": "/images/avatar3.jpg"
        },
        "messages": [
            {"id": "msg6", "text": "711。取。", "sender": "rider", "timestamp": "2023-10-26T09:58:00.000Z"}
        ]
    },
    "chat_rider_4": {
        "rider": {
            "id": "rider_4",
            "name": "送餐员虹夏",
            "avatar": "/images/avatar4.jpg"
        },
        "messages": [
            {"id": "msg7", "text": "您的外卖已经送至青溪4舍楼下寄存点，请及时领取~", "sender": "rider", "timestamp": "2023-10-26T09:58:00.000Z"}
        ]
    }
}

@messages_bp.route('/list', methods=['POST', 'OPTIONS'])
@token_required
def get_chat_list(current_user):
    """获取聊天列表"""
    try:
        # 组合聊天数据和骑手信息
        chat_list = []
        for chat in CHATS_DATA:
            rider = RIDERS_DATA.get(chat['riderId'])
            if rider:
                chat_with_rider = {
                    **chat,
                    'rider': rider,
                    'timestamp': (datetime.now() - timedelta(minutes=chat['minutesAgo'])).isoformat()
                }
                chat_list.append(chat_with_rider)
        
        # 按时间排序
        chat_list.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return success_response(chat_list)
    except Exception as e:
        current_app.logger.error(f"获取聊天列表失败: {str(e)}")
        return error_response(f"获取聊天列表失败: {str(e)}")

@messages_bp.route('/<chat_id>/details', methods=['POST', 'OPTIONS'])
@token_required
def get_chat_details(current_user, chat_id):
    """获取特定聊天的详细信息"""
    try:
        if chat_id not in MESSAGES_DATA:
            # 如果聊天记录不存在，尝试从chat_id中提取rider_id创建空聊天
            rider_id = chat_id.replace('chat_', '') if chat_id.startswith('chat_') else None
            if rider_id and rider_id in RIDERS_DATA:
                # 返回空聊天记录，包含骑手信息
                empty_chat_data = {
                    "rider": RIDERS_DATA[rider_id],
                    "messages": []
                }
                return success_response(empty_chat_data)
            else:
                return error_response("聊天记录不存在", 404)
        
        chat_data = MESSAGES_DATA[chat_id]
        return success_response(chat_data)
    except Exception as e:
        current_app.logger.error(f"获取聊天详情失败: {str(e)}")
        return error_response(f"获取聊天详情失败: {str(e)}")

@messages_bp.route('/<chat_id>/send', methods=['POST', 'OPTIONS'])
@token_required
def send_message(current_user, chat_id):
    """发送消息到特定聊天"""
    try:
        data = request.get_json()
        message_text = data.get('message', '').strip()
        
        if not message_text:
            return error_response("消息内容不能为空")
        
        if chat_id not in MESSAGES_DATA:
            return error_response("聊天记录不存在", 404)
        
        # 创建新消息
        new_message = {
            "id": f"msg_user_{int(datetime.now().timestamp() * 1000)}",
            "text": message_text,
            "sender": "user",
            "timestamp": datetime.now().isoformat() + "Z"
        }
        
        # 在实际环境中，这里应该保存到数据库
        # 暂时只返回成功响应
        return success_response({
            'message': new_message,
            'success': True
        })
    except Exception as e:
        current_app.logger.error(f"发送消息失败: {str(e)}")
        return error_response(f"发送消息失败: {str(e)}")

@messages_bp.route('/<chat_id>/mark_read', methods=['POST', 'OPTIONS'])
@token_required
def mark_chat_as_read(current_user, chat_id):
    """标记聊天为已读"""
    try:
        # 在实际环境中，这里应该更新数据库中的未读计数
        # 暂时只返回成功响应
        return success_response({'success': True})
    except Exception as e:
        current_app.logger.error(f"标记已读失败: {str(e)}")
        return error_response(f"标记已读失败: {str(e)}")

@messages_bp.route('/mark_all_read', methods=['POST', 'OPTIONS'])
@token_required
def mark_all_chats_as_read(current_user):
    """标记所有聊天为已读"""
    try:
        # 在实际环境中，这里应该更新数据库中所有聊天的未读计数
        # 暂时只返回成功响应
        return success_response({'success': True})
    except Exception as e:
        current_app.logger.error(f"标记全部已读失败: {str(e)}")
        return error_response(f"标记全部已读失败: {str(e)}")
