from flask import Blueprint, request, jsonify, current_app
from http import HTTPStatus
from dashscope import Application
from utils.response import success_response, error_response

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/', methods=['POST', 'OPTIONS'])
def chat():
    """处理聊天消息 - 普通响应"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        context = data.get('context', '')  # 获取上下文信息
        
        if not user_message:
            return error_response("消息内容不能为空", 400)

        # DashScope配置
        APP_ID = 'b3e19546f961406db58a8f1e3eb55821'
        DASHCOPE_API_KEY = "sk-e6a9b19bd0bc41ba92157f2538bf581a"

        # 根据上下文调整提示词
        if context == 'customer_service':
            system_prompt = """你是ZJU Last1KM平台的专业客服代表。请以友好、专业的态度回答用户问题。

平台信息：
- ZJU Last1KM是浙江大学校园内的配送服务平台
- 主要服务：校园内快递代取、外卖配送、物品代购等
- 服务范围：浙江大学各个校区
- 客服热线：400-123-4567

常见问题处理指南：
1. 订单问题：引导用户查看订单详情页面，提供取消/修改订单的方法
2. 配送问题：解释配送流程，提供配送员联系方式
3. 费用问题：说明费用计算规则，解释配送费构成
4. 退款问题：说明退款流程和时间
5. 技术问题：提供基本故障排除建议

回答要求：
- 语言亲切友好，使用"您"称呼用户
- 回答简洁明了，重点突出
- 必要时提供具体的操作步骤
- 如遇复杂问题，建议联系人工客服

请回答用户的问题："""
            
            full_prompt = f"{system_prompt}\n\n用户问题：{user_message}"
        else:
            full_prompt = user_message

        # 调用DashScope API
        responses = Application.call(
            app_id=APP_ID,
            api_key=DASHCOPE_API_KEY,
            prompt=full_prompt,
            stream=False  # 关闭流式传输
        )
        
        # 处理响应
        if responses.status_code == HTTPStatus.OK:
            reply_text = responses.output.text if responses.output else '抱歉，我没能理解您的问题，请重新描述或联系人工客服。'
            return success_response({'reply': reply_text})
        else:
            error_message = f"AI服务错误: {responses.code} - {responses.message}"
            current_app.logger.error(f"DashScope error: {error_message} (request_id: {responses.request_id})")
            
            # 返回友好的错误信息
            return success_response({
                'reply': '抱歉，客服系统暂时繁忙，请稍后再试或直接拨打客服热线：400-123-4567'
            })

    except Exception as e:
        current_app.logger.error(f"聊天处理错误: {str(e)}")
        if hasattr(e, 'request_id'):
            current_app.logger.error(f"DashScope request_id: {e.request_id}")
        
        # 返回友好的错误信息而不是抛出异常
        return success_response({
            'reply': '抱歉，系统出现了问题，请稍后重试或拨打客服热线：400-123-4567获取帮助。'
        })

@chat_bp.route('/test', methods=['GET'])
def test_chat():
    """测试聊天接口"""
    return success_response({'message': '聊天接口正常工作'})