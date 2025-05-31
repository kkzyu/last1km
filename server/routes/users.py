from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
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
                setattr(current_user, field, data[field])
        
        db.session.commit()
        return success_response(current_user.to_dict(), "资料更新成功")
        
    except Exception as e:
        return error_response(f"更新用户资料失败: {str(e)}")

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
