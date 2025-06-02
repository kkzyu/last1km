from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

def token_required(f):
    """JWT token验证装饰器"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        try:
            # 获取当前用户ID
            current_user_id = get_jwt_identity()
            
            if not current_user_id:
                return jsonify({
                    'success': False,
                    'message': '无效的token'
                }), 401
            
            # 查询用户
            current_user = User.query.get(current_user_id)
            if not current_user:
                return jsonify({
                    'success': False,
                    'message': '用户不存在'
                }), 401
            
            # 将当前用户传递给被装饰的函数
            return f(current_user, *args, **kwargs)
            
        except Exception as e:
            current_app.logger.error(f"Token验证错误: {str(e)}")
            return jsonify({
                'success': False,
                'message': '认证失败'
            }), 401
    
    return decorated_function

def admin_required(f):
    """管理员权限验证装饰器"""
    @wraps(f)
    @token_required
    def decorated_function(current_user, *args, **kwargs):
        # 检查用户是否是管理员（这里假设有is_admin字段）
        if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': '需要管理员权限'
            }), 403
        
        return f(current_user, *args, **kwargs)
    
    return decorated_function