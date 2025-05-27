from functools import wraps
from flask import request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt
from models.user import User
from utils.response import error_response

def token_required(f):
    """
    JWT token验证装饰器（备用方案，推荐直接使用 @jwt_required()）
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return error_response("用户不存在", 401)
            if current_user.status != 'active':
                return error_response("用户账户已被禁用", 401)
            return f(current_user, *args, **kwargs)
        except Exception as e:
            return error_response("token验证失败", 401)
    return decorated

def get_current_user():
    """
    获取当前登录用户
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return None
        current_user = User.query.get(current_user_id)
        return current_user
    except:
        return None

def admin_required(f):
    """
    管理员权限验证装饰器
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return error_response("用户不存在", 401)
            if current_user.status != 'active':
                return error_response("用户账户已被禁用", 401)
            # 假设有一个is_admin字段或者role字段
            # if not current_user.is_admin:
            #     return error_response("需要管理员权限", 403)
            return f(current_user, *args, **kwargs)
        except Exception as e:
            return error_response("权限验证失败", 401)
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