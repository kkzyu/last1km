from functools import wraps
from flask import request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models.user import User
from utils.response import error_response

def token_required(f):
    """JWT token验证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return error_response("用户不存在", 401)
            return f(current_user, *args, **kwargs)
        except Exception as e:
            return error_response("token验证失败", 401)
    return decorated
