from flask import Blueprint, request, current_app # 新增 current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.user import User
from models.order import Order
from models.address import Address
# যেহেতু您还没有配送员后端，我们将不会从 models.deliverer 导入
# from models.deliverer import Deliverer 
from utils.response import success_response, error_response
from utils.auth_helpers import token_required
from datetime import datetime
import os 
import uuid 
import traceback
from werkzeug.utils import secure_filename


from services.ai_service import ai_service

orders_bp = Blueprint('orders', __name__)


# --- 图片上传路由 (保持您提供的版本) ---
@orders_bp.route('/upload_image', methods=['POST', 'OPTIONS'])
@token_required
def upload_order_image(current_user):
    try:
        current_app.logger.info(f"User {current_user.id} attempting to upload image.")
        
        # 检查是否有文件
        if 'image' not in request.files:
            current_app.logger.warning("No image file provided in request")
            return error_response("未提供图片文件", 400)
        
        file = request.files['image']
        if file.filename == '':
            current_app.logger.warning("Empty filename provided")
            return error_response("未选择文件", 400)

        if file:
            filename = secure_filename(file.filename)
            ext = ''
            if '.' in filename:
                ext = filename.rsplit('.', 1)[1].lower()
            
            allowed_extensions = {'png', 'jpg', 'jpeg'}
            if ext not in allowed_extensions:
                current_app.logger.warning(f"Invalid file extension: {ext}")
                return error_response(f"无效的图片类型。只允许: {', '.join(allowed_extensions)}", 400)
            
            unique_filename = str(uuid.uuid4()) + "." + ext
            
            upload_folder = current_app.config.get('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'server/static/uploads'))
            current_app.logger.info(f"Upload folder: {upload_folder}")
            
            if not os.path.exists(upload_folder):
                try:
                    os.makedirs(upload_folder, exist_ok=True)
                    current_app.logger.info(f"Created upload directory: {upload_folder}")
                except OSError as e:
                    current_app.logger.error(f"Failed to create upload directory: {str(e)}")
                    return error_response(f"创建上传目录失败: {str(e)}", 500)

            file_path = os.path.join(upload_folder, unique_filename)
            current_app.logger.info(f"Saving file to: {file_path}")
            
            try:
                file.save(file_path)
                current_app.logger.info(f"File saved successfully: {file_path}")
                return success_response({
                    "filename": unique_filename,
                    "filePath": f"/static/uploads/{unique_filename}" 
                }, "图片上传成功")
            except Exception as e:
                current_app.logger.error(f"保存图片失败: {str(e)}")
                return error_response(f"保存图片失败: {str(e)}", 500)
                
        return error_response("图片上传失败", 500)
    
    except Exception as e:
        current_app.logger.error(f"Unexpected error in upload_order_image: {str(e)}")
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return error_response(f"图片上传过程中发生错误: {str(e)}", 500)

@orders_bp.route('/analyze-image', methods=['POST'])
@token_required
def analyze_order_image(current_user):
    """分析订单图片，提取商品描述和取件信息"""
    try:
        data = request.get_json()
        filename = data.get('filename')
        
        if not filename:
            return success_response({}, "请提供图片文件名", success=False)
        
        # 构建图片完整路径
        upload_folder = current_app.config.get('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'server/static/uploads'))
        image_path = os.path.join(upload_folder, filename)
        
        # 检查文件是否存在
        if not os.path.exists(image_path):
            return success_response({}, "图片文件不存在", success=False)
        
        # 执行OCR识别
        recognized_text = ai_service.recognize_text(image_path)
        
        # 解析订单信息
        parsed_info = ai_service.parse_order_info(recognized_text)
        
        return success_response({
            'recognizedText': recognized_text,  # 原始识别文本，可用于调试
            'description': parsed_info['description'],
            'orderInfo': parsed_info['orderInfo']
        })
        
    except Exception as error:
        current_app.logger.error(f'AI分析错误: {str(error)}')
        # 返回正确的错误响应，避免401状态码
        return error_response(f'AI分析失败: {str(error)}', 500)
    
# --- 创建订单 (保持您提供的版本，确保 Order 模型字段正确) ---
@orders_bp.route('/', methods=['POST', 'OPTIONS']) # 添加 OPTIONS
@token_required
def create_order(current_user):
    try:
        data = request.get_json()
        
        if not data:
            return error_response("请求数据不能为空")
        
        # 处理单个订单或订单列表
        requests_data = data if isinstance(data, list) else [data]
        
        if not requests_data:
            return error_response("订单数据不能为空")
        
        created_orders = []
        
        for request_data in requests_data:
            # 验证必填字段
            required_fields = ['origin', 'destination', 'amount']
            for field in required_fields:
                if not request_data.get(field):
                    return error_response(f"缺少必填字段: {field}")
            
            # 验证金额
            try:
                amount = float(request_data['amount'])
                if amount <= 0:
                    return error_response("委托金额必须大于0")
            except (ValueError, TypeError):
                return error_response("委托金额格式错误")
            
            # 创建订单
            order = Order(
                user_id=current_user.id,
                origin=request_data['origin'],
                destination=request_data['destination'],
                origin_detail=request_data.get('origin_detail', ''),
                destination_detail=request_data.get('destination_detail', ''),
                description=request_data.get('description', ''),
                order_info=request_data.get('order_info', ''),
                amount=amount,
                status='pending',
                image=request_data.get('image'),
                origin_lat=request_data.get('origin_lat'),
                origin_lng=request_data.get('origin_lng'),
                dest_lat=request_data.get('dest_lat'),
                dest_lng=request_data.get('dest_lng'),
                estimated_duration=request_data.get('estimated_duration'),
                estimated_distance=request_data.get('estimated_distance')
            )
            
            db.session.add(order)
            db.session.flush()  # 获取订单ID
            
            created_orders.append(order.to_dict())
        
        db.session.commit()
        
        return success_response({
            'orders': created_orders,
            'count': len(created_orders)
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"创建订单失败: {str(e)}")
        return error_response(f"创建订单失败: {str(e)}")

# --- 获取订单列表 (保持您提供的版本) ---
@orders_bp.route('/', methods=['GET', 'OPTIONS']) # 添加 OPTIONS
@token_required
def get_orders(current_user):
    """获取订单列表 (只包含进行中、已完成、已取消状态)"""
    try:
        # 确保 Order 模型中的 order_status 字段实际存储的是这些英文值
        allowed_statuses = ['pending', 'completed', 'cancelled'] 
        orders = Order.query.filter_by(user_id=current_user.id)\
                            .filter(Order.order_status.in_(allowed_statuses))\
                            .order_by(Order.created_at.desc())\
                            .all()
        return success_response([order.to_dict() for order in orders])
    except Exception as e:
        current_app.logger.error(f"获取订单列表失败: {str(e)}")
        return error_response(f"获取订单列表失败: {str(e)}")

# --- 修改后的获取订单详情函数 ---
@orders_bp.route('/<int:order_id>', methods=['GET', 'OPTIONS']) # 添加 OPTIONS
@token_required
def get_order(current_user, order_id):
    """获取订单详情，并伪造配送员信息（如果订单已分配）"""
    try:
        order_instance = Order.query.get(order_id) # 使用 order_instance 避免与内部变量冲突
        if not order_instance:
            return error_response("订单不存在", 404)
        
        # 权限检查：目前仅订单创建者可访问
        # 未来您可以扩展此逻辑以允许配送员访问其被分配的订单
        if order_instance.user_id != current_user.id:
            return error_response("无权访问该订单", 403)
            
        order_data = order_instance.to_dict() # 获取订单基本数据

        # 检查订单是否有 deliverer_id (假设您的 Order 模型有此字段)
        if hasattr(order_instance, 'deliverer_id') and order_instance.deliverer_id:
            # 伪造配送员信息
            order_data['deliverer'] = {
                'id': order_instance.deliverer_id, # 可以使用订单中的 deliverer_id
                'name': "喜多郁代", # 您要求的姓名
                'avatar': "/static/avatars/aviator1.jpg", # 编造一个头像路径
                                                                    # 请确保您在 static 目录下有此图片，或使用一个网络图片URL
                                                                    # 例如：'https://via.placeholder.com/100'
                'rating': 4.8, # 编造一个评分
                'phone': '13800138000' # 编造一个电话号码 (可选，根据前端是否需要)
                # 您可以根据前端 OrderDetailView.vue 中对 deliverer 对象的期望来添加更多伪造字段
            }
        else:
            order_data['deliverer'] = None # 该订单没有关联的配送员

        return success_response(order_data)
        
    except Exception as e:
        current_app.logger.error(f"获取订单详情失败 (ID: {order_id}): {str(e)}")
        return error_response(f"获取订单详情失败: {str(e)}")


# --- 其他订单操作路由 (cancel, review, delete) 保持您提供的版本 ---
@orders_bp.route('/<int:order_id>/cancel', methods=['POST', 'OPTIONS']) # 添加 OPTIONS
@token_required
def cancel_order(current_user, order_id):
    """取消订单 (目标：进行中 -> 已取消)"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return error_response("订单不存在", 404)
        if order.user_id != current_user.id:
            return error_response("无权取消该订单", 403)
        # 确保 order_status 与数据库中的值一致 ('pending' 或中文 '进行中')
        if order.order_status != 'pending': 
            return error_response(f"只有进行中(pending)的订单才能取消, 当前状态: {order.order_status}")
        
        order.order_status = 'cancelled' # 更新为 'cancelled' 或对应中文
        order.cancelled_at = datetime.utcnow()
        db.session.commit()
        return success_response(order.to_dict(), message="订单已取消")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"取消订单失败: {str(e)}")
        return error_response(f"取消订单失败: {str(e)}")


@orders_bp.route('/<int:order_id>/review', methods=['POST', 'OPTIONS']) # 添加 OPTIONS
@token_required
def review_order(current_user, order_id):
    """评价订单 (目标：已完成的订单)"""
    try:
        data = request.get_json()
        rating = data.get('rating')
        comment = data.get('comment')

        if rating is None or comment is None:
            return error_response("评价内容不完整")

        order = Order.query.get(order_id)
        if not order:
            return error_response("订单不存在", 404)
        if order.user_id != current_user.id:
            return error_response("无权评价该订单", 403)
        # 确保 order_status 与数据库中的值一致 ('completed' 或中文 '已完成')
        if order.order_status != 'completed':
            return error_response(f"只能评价已完成的订单, 当前状态: {order.order_status}")
            
        order.user_review = {
            'rating': int(rating),
            'comment': str(comment),
            'reviewed_at': datetime.utcnow().isoformat()
        }
        db.session.commit()
        return success_response(order.to_dict(), message="评价成功")
    except ValueError:
        db.session.rollback()
        return error_response("评级必须是数字")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"评价失败: {str(e)}")
        return error_response(f"评价失败: {str(e)}")

@orders_bp.route('/<int:order_id>', methods=['DELETE', 'OPTIONS']) # 为 deleteOrder 添加 OPTIONS
@token_required
def delete_order(current_user, order_id):
    """删除订单 (目标：已取消的订单)"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return error_response("订单不存在", 404)
        if order.user_id != current_user.id:
            return error_response("无权删除该订单", 403)
        # 确保 order_status 与数据库中的值一致 ('cancelled' 或中文 '已取消')
        if order.order_status != 'cancelled':
            return error_response(f"只能删除已取消的订单, 当前状态: {order.order_status}", 403)

        db.session.delete(order)
        db.session.commit()
        return success_response(message="订单已删除")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"删除订单失败: {str(e)}")
        return error_response(f"删除订单失败: {str(e)}")


@orders_bp.route('/<int:order_id>/complete', methods=['POST', 'OPTIONS']) # 为 completeOrder 添加 OPTIONS
@token_required
def complete_order(current_user, order_id):
    """标记订单为已完成"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return error_response("订单不存在", 404)
        if order.user_id != current_user.id:
            return error_response("无权操作该订单", 403)
        if order.order_status != 'pending':
            return error_response(f"只有进行中的订单才能标记为已完成, 当前状态: {order.order_status}")
            
        order.order_status = 'completed'
        order.completed_at = datetime.utcnow()
        db.session.commit()
        return success_response(order.to_dict(), message="订单已完成")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"完成订单失败: {str(e)}")
        return error_response(f"完成订单失败: {str(e)}")
    


