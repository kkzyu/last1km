from flask import Blueprint, request
from models import db
from models.user import User
from models.address import Address
from utils.response import success_response, error_response
from utils.auth_helpers import token_required

users_bp = Blueprint('users', __name__)

@users_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """获取用户资料"""
    return success_response(current_user.to_dict())

@users_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    """更新用户资料"""
    try:
        data = request.get_json()
        
        # 更新允许修改的字段
        updatable_fields = ['nickname', 'gender', 'school_info', 'dormitory', 'phone']
        for field in updatable_fields:
            if field in data:
                setattr(current_user, field, data[field])
        
        db.session.commit()
        
        return success_response(current_user.to_dict(), "资料更新成功")
        
    except Exception as e:
        return error_response(f"更新资料失败: {str(e)}")

@users_bp.route('/addresses', methods=['GET'])
@token_required
def get_addresses(current_user):
    """获取用户地址列表"""
    try:
        addresses = Address.query.filter_by(user_id=current_user.id).all()
        return success_response([addr.to_dict() for addr in addresses])
    except Exception as e:
        return error_response(f"获取地址列表失败: {str(e)}")

@users_bp.route('/addresses', methods=['POST'])
@token_required
def add_address(current_user):
    """添加地址"""
    try:
        data = request.get_json()
        
        required_fields = ['address_type', 'address_name', 'detailed_address']
        for field in required_fields:
            if not data.get(field):
                return error_response(f"{field} 不能为空")
        
        address = Address(
            user_id=current_user.id,
            address_type=data['address_type'],
            address_name=data['address_name'],
            detailed_address=data['detailed_address'],
            is_default=data.get('is_default', False)
        )
        
        db.session.add(address)
        db.session.commit()
        
        return success_response(address.to_dict(), "地址添加成功")
        
    except Exception as e:
        return error_response(f"添加地址失败: {str(e)}")
    
# 在现有的users_bp.route下添加以下路由函数

@users_bp.route('/addresses/<int:address_id>', methods=['PUT'])
@token_required
def update_address(current_user, address_id):
    """更新地址"""
    try:
        data = request.get_json()
        
        # 检查地址是否存在且属于当前用户
        address = Address.query.filter_by(id=address_id, user_id=current_user.id).first()
        if not address:
            return error_response("地址不存在或无权修改", 404)
        
        # 更新字段
        if 'address_type' in data:
            address.address_type = data['address_type']
        if 'address_detail' in data:
            address.address_detail = data['address_detail']
        if 'notes' in data:
            address.notes = data['notes']
        if 'is_default' in data and data['is_default']:
            # 如果设为默认，需要将其他地址的默认状态取消
            if data['is_default']:
                Address.query.filter_by(user_id=current_user.id, is_default=True).update({'is_default': False})
            address.is_default = data['is_default']
        
        db.session.commit()
        return success_response(address.to_dict(), "地址更新成功")
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"更新地址失败: {str(e)}")

@users_bp.route('/addresses/<int:address_id>', methods=['DELETE'])
@token_required
def delete_address(current_user, address_id):
    """删除地址"""
    try:
        # 检查地址是否存在且属于当前用户
        address = Address.query.filter_by(id=address_id, user_id=current_user.id).first()
        if not address:
            return error_response("地址不存在或无权删除", 404)
        
        db.session.delete(address)
        db.session.commit()
        
        return success_response(None, "地址删除成功")
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"删除地址失败: {str(e)}")