from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request
from services.auth_service import AuthService

def token_required(f):
    """token验证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'code': 401, 'message': 'Token格式错误'}), 401
        
        if not token:
            return jsonify({'code': 401, 'message': '未提供认证token'}), 401
        
        current_user = AuthService.verify_token(token)
        if not current_user:
            return jsonify({'code': 401, 'message': 'Token无效或已过期'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def admin_required(f):
    """管理员权限验证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'code': 401, 'message': 'Token格式错误'}), 401
        
        if not token:
            return jsonify({'code': 401, 'message': '未提供认证token'}), 401
        
        current_user = AuthService.verify_token(token)
        if not current_user:
            return jsonify({'code': 401, 'message': 'Token无效或已过期'}), 401
        
        # 检查是否是管理员 (这里假设有一个role字段或者特定的管理员判断逻辑)
        if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
            return jsonify({'code': 403, 'message': '权限不足'}), 403
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def validate_user_status(user):
    """
    验证用户状态
    """
    if not user:
        return False, "用户不存在"
    if user.status != 'active':
        return False, "用户账户已被禁用"
    return True, "用户状态正常"

def check_token_freshness():
    """
    检查token是否是新鲜的（用于敏感操作）
    """
    try:
        jwt_data = get_jwt()
        return jwt_data.get('fresh', False)
    except:
        return False