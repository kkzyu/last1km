from flask import Blueprint, request, jsonify, current_app, Response, stream_with_context
from http import HTTPStatus
from dashscope import Application
from models.chat_message import ChatMessage
from models.user import User
from models.order import Order
from models import db
from utils.response import success_response, error_response
from utils.auth_helpers import token_required  # 改为使用 auth_helpers
import json

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/', methods=['POST', 'OPTIONS'])
@token_required
def chat(current_user):
    """处理聊天消息 - 带用户认证和历史记录 (流式传输)"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()

        if not user_message:
            return error_response("消息内容不能为空", 400)

        # 保存用户消息到数据库
        user_chat_message = ChatMessage(
            user_id=current_user.id,
            sender_type='user',
            message_content=user_message
        )
        db.session.add(user_chat_message)
        db.session.commit()

        # 获取用户历史聊天记录（最近20条）
        chat_history = ChatMessage.query.filter_by(
            user_id=current_user.id
        ).order_by(ChatMessage.timestamp.desc()).limit(20).all()
        chat_history.reverse()  # 时间正序

        # 获取用户信息用于上下文 (使用 getattr 保证安全访问)
        user_info = {
            'username': current_user.username,
            'nickname': getattr(current_user, 'nickname', None),
            'gender': getattr(current_user, 'gender', None),
            'phone': getattr(current_user, 'phone', None),
            'school_info': getattr(current_user, 'school_info', None),
            'dormitory': getattr(current_user, 'dormitory', None)
        }

        # 获取用户订单信息（最近5条）
        user_orders = Order.query.filter_by(
            user_id=current_user.id
        ).order_by(Order.created_at.desc()).limit(5).all()

        # DashScope配置 (建议将这些配置移到 config.py 或环境变量中)
        APP_ID = current_app.config.get('DASHSCOPE_APP_ID', 'b3e19546f961406db58a8f1e3eb55821')
        DASHCOPE_API_KEY = current_app.config.get('DASHSCOPE_API_KEY', "sk-e6a9b19bd0bc41ba92157f2538bf581a")

        # 构建系统提示词
        system_prompt = f"""你是ZJU Last1KM平台的专业客服代表。请以友好、专业的态度回答用户问题。

平台信息：
- ZJU Last1KM是浙江大学校园内的配送服务平台
- 主要服务：校园内快递代取、外卖配送、物品代购等
- 服务范围：浙江大学各个校区
- 客服热线：400-123-4567 (此为示例，请替换为真实号码)

当前用户信息：
- 用户名：{user_info['username']}
- 昵称：{user_info['nickname'] or '未设置'}
- 性别：{user_info['gender'] or '未设置'}
- 联系电话：{user_info['phone'] or '未设置'}
- 学校信息：{user_info['school_info'] or '未设置'}
- 宿舍信息：{user_info['dormitory'] or '未设置'}

用户最近订单信息："""

        if user_orders:
            for i, order in enumerate(user_orders, 1):
                # 确保使用 Order 模型中正确的字段名，并使用 getattr 安全访问
                system_prompt += f"""
订单{i}：
- 订单ID：{order.id}
- 状态：{getattr(order, 'order_status', '未知状态')}
- 起点：{getattr(order, 'start_address', '未提供')}
- 终点：{getattr(order, 'end_address', '未提供')}
- 描述：{getattr(order, 'item_description', '无描述')}
- 金额：{getattr(order, 'total_amount', 0.0):.2f}元
- 创建时间：{order.created_at.strftime('%Y-%m-%d %H:%M') if order.created_at else '未知时间'}"""
        else:
            system_prompt += "\n该用户暂无订单记录。"

        system_prompt += """

聊天历史记录："""
        
        if len(chat_history) > 1:  # 排除刚刚添加的用户消息
            for msg in chat_history[:-1]:
                role = "用户" if msg.sender_type == "user" else "客服"
                system_prompt += f"\n{role}：{msg.message_content}"
        else:
            system_prompt += "\n这是用户的首次咨询。"

        system_prompt += """

常见问题处理指南：
1. 订单问题：基于用户的实际订单信息回答，可以引用具体的订单ID和状态。
2. 配送问题：解释配送流程，如果平台有配送员信息，可以考虑是否提供（注意隐私）。
3. 费用问题：说明费用计算规则，解释配送费构成。
4. 退款问题：说明退款流程和时间。
5. 技术问题：提供基本故障排除建议。
6. 个人信息：可以根据用户资料提供个性化建议，但避免泄露过多敏感信息。

回答要求：
- 语言亲切友好，可以称呼用户的昵称或用户名。
- 回答简洁明了，重点突出。
- 基于用户实际信息和订单状态提供准确回答。
- 必要时提供具体的操作步骤。
- 如遇复杂问题，建议联系人工客服。
- 如果用户询问具体订单，可以引用订单ID和相关信息。

请回答用户的问题："""

        full_prompt = f"{system_prompt}\n\n用户当前问题：{user_message}"
        current_app.logger.debug(f"Full prompt for DashScope: {full_prompt[:500]}...")

        def generate_responses():
            accumulated_reply = ""
            try:
                responses = Application.call(
                    app_id=APP_ID,
                    api_key=DASHCOPE_API_KEY,
                    prompt=full_prompt,
                    stream=True  # 启用流式输出
                )

                for response_chunk in responses:
                    if response_chunk.status_code == HTTPStatus.OK:
                        chunk_text = response_chunk.output.text if response_chunk.output and response_chunk.output.text else ''
                        accumulated_reply += chunk_text
                        # SSE format: data: {...}\n\n
                        yield f"data: {json.dumps({'chunk': chunk_text})}\n\n"
                    else:
                        error_message_chunk = f"AI服务流式响应错误: Code {response_chunk.code} - {response_chunk.message}"
                        current_app.logger.error(f"DashScope stream error: {error_message_chunk} (request_id: {response_chunk.request_id})")
                        yield f"data: {json.dumps({'error': error_message_chunk, 'final_chunk': True})}\n\n"
                        # 保存部分回复（如果已有）或错误提示
                        if not accumulated_reply:
                             accumulated_reply = '抱歉，客服机器人暂时开小差了，请稍后再试或直接拨打客服热线。'
                        break 
                
                # 流结束后，保存完整的AI回复
                if accumulated_reply:
                    ai_chat_message = ChatMessage(
                        user_id=current_user.id,
                        sender_type='agent',
                        message_content=accumulated_reply.strip() # 去除可能存在的末尾空字符
                    )
                    db.session.add(ai_chat_message)
                    db.session.commit()
                yield f"data: {json.dumps({'message': 'Stream ended', 'final_chunk': True})}\n\n"

            except Exception as e_stream:
                current_app.logger.error(f"DashScope流处理错误: {str(e_stream)}", exc_info=True)
                error_reply = '抱歉，处理您的请求时发生流错误，请稍后再试。'
                yield f"data: {json.dumps({'error': error_reply, 'final_chunk': True})}\n\n"
                # 尝试保存错误信息
                try:
                    if not accumulated_reply: # 如果流开始前就出错，accumulated_reply可能为空
                        accumulated_reply = error_reply
                    
                    error_save_message = ChatMessage(
                        user_id=current_user.id,
                        sender_type='agent',
                        message_content=accumulated_reply.strip() if accumulated_reply else error_reply
                    )
                    db.session.add(error_save_message)
                    db.session.commit()
                except Exception as db_error_stream:
                    current_app.logger.error(f"保存流错误回复到数据库失败: {str(db_error_stream)}")
                    db.session.rollback()

        return Response(stream_with_context(generate_responses()), mimetype='text/event-stream')

    except Exception as e:
        current_app.logger.error(f"聊天处理错误 (非流部分): {str(e)}", exc_info=True)
        # 这种错误通常在流开始前发生，因此直接返回JSON错误
        # 但为了客户端统一处理，也可以考虑返回SSE错误事件
        # 这里我们保持原有逻辑，返回JSON错误，因为流尚未启动
        
        reply_text = '抱歉，系统发生内部错误，我们正在紧急处理。请稍后再试或联系人工客服。'
        
        try:
            error_save_message = ChatMessage(
                user_id=current_user.id, 
                sender_type='agent',
                message_content=reply_text
            )
            db.session.add(error_save_message)
            db.session.commit()
        except Exception as db_error:
            current_app.logger.error(f"保存主错误回复到数据库失败: {str(db_error)}")
            db.session.rollback()
        
        # 对于非流启动前的错误，返回JSON错误响应更合适
        return error_response(reply_text, 500)

@chat_bp.route('/history', methods=['GET'])
@token_required
def get_chat_history(current_user):
    """获取用户聊天历史记录"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        chat_messages_pagination = ChatMessage.query.filter_by(
            user_id=current_user.id
        ).order_by(ChatMessage.timestamp.asc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        messages_data = [msg.to_dict() for msg in chat_messages_pagination.items]
        
        return success_response({
            'messages': messages_data,
            'pagination': {
                'page': chat_messages_pagination.page,
                'per_page': chat_messages_pagination.per_page,
                'total_items': chat_messages_pagination.total,
                'total_pages': chat_messages_pagination.pages,
                'has_next': chat_messages_pagination.has_next,
                'has_prev': chat_messages_pagination.has_prev
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"获取聊天历史失败: {str(e)}", exc_info=True)
        return error_response("获取聊天历史失败", 500)

@chat_bp.route('/clear', methods=['DELETE'])
@token_required
def clear_chat_history(current_user):
    """清空用户聊天历史记录"""
    try:
        deleted_count = ChatMessage.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        current_app.logger.info(f"用户 {current_user.id} 清空了 {deleted_count} 条聊天记录。")
        return success_response({'message': '聊天记录已清空'})
        
    except Exception as e:
        current_app.logger.error(f"清空聊天历史失败: {str(e)}", exc_info=True)
        db.session.rollback()
        return error_response("清空聊天历史失败", 500)

@chat_bp.route('/test', methods=['GET'])
def test_chat_endpoint(): # Renamed function to avoid conflict if old 'test_chat' was imported elsewhere
    """测试聊天接口是否可达"""
    return success_response({'message': '聊天接口服务正常运行'})