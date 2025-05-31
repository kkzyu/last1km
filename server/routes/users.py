from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
import uuid
from models import db
from models.user import User
from models.address import Address
from utils.response import success_response, error_response
from utils.auth_helpers import token_required

users_bp = Blueprint('users', __name__)

@users_bp.route('/profile', methods=['GET', 'OPTIONS'])
@token_required
def get_profile(current_user):
    """获取用户资料"""
    try:
        return success_response(current_user.to_dict())
    except Exception as e:
        return error_response(f"获取用户资料失败: {str(e)}")

@users_bp.route('/profile', methods=['PUT', 'OPTIONS'])
@token_required
def update_profile(current_user):
    """更新用户资料"""
    try:
        data = request.get_json()
        
        # 更新可修改的字段
        allowed_fields = ['nickname', 'avatar', 'gender', 'school_info', 'dormitory', 'phone']
        for field in allowed_fields:
            if field in data:
                # For avatar, this route expects a filename string, not a file upload.
                # Actual file upload is handled by /upload_avatar
                setattr(current_user, field, data[field])
        
        db.session.commit()
        return success_response(current_user.to_dict(), "资料更新成功")
        
    except Exception as e:
        return error_response(f"更新用户资料失败: {str(e)}")

@users_bp.route('/upload_avatar', methods=['POST'])
@token_required
def upload_avatar_route(current_user):
    """用户上传头像"""
    if 'avatar' not in request.files:
        return error_response("未找到头像文件", 400)
    
    file = request.files['avatar']
    if file.filename == '':
        return error_response("未选择文件", 400)

    if file:
        filename = secure_filename(file.filename)
        _root, ext = os.path.splitext(filename)
        allowed_extensions = ['.png', '.jpg', '.jpeg']
        if ext.lower() not in allowed_extensions:
            return error_response(f"无效的文件类型。仅允许: {', '.join(allowed_extensions)}", 400)

        # 检查文件大小 (示例: 2MB)
        # MAX_AVATAR_SIZE = 2 * 1024 * 1024 
        # if file.content_length > MAX_AVATAR_SIZE:
        #     return error_response("文件过大，请上传小于2MB的图片", 400)

        unique_filename = f"avatar_{current_user.id}_{uuid.uuid4().hex}{ext}"
        
        upload_folder = current_app.config.get('UPLOAD_FOLDER')
        if not upload_folder:
            current_app.logger.error("UPLOAD_FOLDER 未在配置中设置。")
            return error_response("服务器配置错误：上传路径未设置", 500)

        if not os.path.exists(upload_folder):
            try:
                os.makedirs(upload_folder, exist_ok=True)
            except OSError as e:
                current_app.logger.error(f"创建上传目录失败: {e}")
                return error_response(f"创建上传目录失败: {str(e)}", 500)
        
        file_path = os.path.join(upload_folder, unique_filename)
        
        try:
            # 删除旧头像文件（如果存在且不是默认头像）
            if current_user.avatar and not current_user.avatar.startswith('default'): # 假设默认头像名以 'default' 开头
                old_avatar_path = os.path.join(upload_folder, current_user.avatar)
                if os.path.exists(old_avatar_path):
                    os.remove(old_avatar_path)
            
            file.save(file_path)
            current_user.avatar = unique_filename  # 在数据库中存储新的文件名
            db.session.commit()
            
            return success_response({
                "message": "头像上传成功",
                "filename": unique_filename, # 后端返回文件名
                "user": current_user.to_dict() # 返回更新后的用户信息
            })
        except Exception as e:
            current_app.logger.error(f"保存头像或更新数据库失败: {e}")
            return error_response(f"头像上传处理失败: {str(e)}", 500)
            
    return error_response("头像上传失败", 500)

@users_bp.route('/addresses', methods=['GET', 'OPTIONS'])
@token_required
def get_addresses(current_user):
    """获取用户的地址列表"""
    try:
        addresses = Address.query.filter_by(user_id=current_user.id).all()
        return success_response([addr.to_dict() for addr in addresses])
    except Exception as e:
        return error_response(f"获取地址列表失败: {str(e)}")

@users_bp.route('/addresses', methods=['POST', 'OPTIONS'])
@token_required
def add_address(current_user):
    """添加新地址"""
    try:
        data = request.get_json()
        address_type = data.get('address_type')
        address_name = data.get('address_name')
        detailed_address = data.get('detailed_address')
        is_default = data.get('is_default', False)
        
        if not all([address_type, address_name, detailed_address]):
            return error_response("地址信息不完整")
        
        address = Address(
            user_id=current_user.id,
            address_type=address_type,
            address_name=address_name,
            detailed_address=detailed_address,
            is_default=is_default
        )
        
        # 如果设为默认地址，需要取消同类型其他默认地址
        if is_default:
            Address.query.filter_by(
                user_id=current_user.id,
                address_type=address_type,
                is_default=True
            ).update({'is_default': False})
        
        db.session.add(address)
        db.session.commit()
        
        return success_response(address.to_dict(), "地址添加成功")
        
    except Exception as e:
        return error_response(f"添加地址失败: {str(e)}")
