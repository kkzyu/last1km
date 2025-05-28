from functools import wraps
from flask import request, Response, current_app # Import current_app for logging
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, exceptions as jwt_exceptions # Import jwt_exceptions
from models.user import User
from utils.response import error_response

def token_required(f):
    """JWT token验证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        # Handle OPTIONS request for CORS preflight
        if request.method == 'OPTIONS':
            return Response(status=200) # Allow preflight
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                current_app.logger.warning(f"User not found for ID: {current_user_id} from token.")
                return error_response("用户不存在或token无效", 401)
            return f(current_user, *args, **kwargs)
        except jwt_exceptions.NoAuthorizationError as e:
            current_app.logger.warning(f"No Authorization header: {str(e)}")
            return error_response("请求未包含授权信息", 401)
        except jwt_exceptions.InvalidHeaderError as e:
            current_app.logger.warning(f"Invalid Authorization header: {str(e)}")
            return error_response("无效的授权头部", 401)
        except jwt_exceptions.ExpiredSignatureError as e:
            current_app.logger.info(f"Token has expired: {str(e)}")
            return error_response("token已过期", 401)
        except jwt_exceptions.DecodeError as e: # Catch generic decode errors
            current_app.logger.warning(f"Token decode error: {str(e)}")
            return error_response("token解码失败", 401)
        except jwt_exceptions.InvalidTokenError as e: # Catch other invalid token errors
            current_app.logger.warning(f"Invalid token: {str(e)}")
            return error_response("token无效", 401)
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred during token verification: {str(e)}")
            return error_response("token验证失败", 401)
    return decorated
