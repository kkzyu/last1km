from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from utils.response import success_response, error_response
import re # 导入 re模块用于正则表达式校验

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    """用户注册"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        phone = data.get('phone') # 获取手机号

        if not username or not password or not phone: # 确保所有字段都已提供
            return error_response("用户名、密码和手机号均不能为空")

        # 密码安全性验证
        if len(password) < 8:
            return error_response("密码长度至少为8位")
        if not re.search(r"[a-z]", password):
            return error_response("密码必须包含至少一个小写字母")
        if not re.search(r"[A-Z]", password):
            return error_response("密码必须包含至少一个大写字母")
        if not re.search(r"\d", password):
            return error_response("密码必须包含至少一位数字")
        # 您可以根据需要添加更多规则，例如特殊字符:
        # if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        #     return error_response("密码必须包含至少一个特殊字符")

        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return error_response("用户名已存在")

        # 检查手机号是否已存在 (假设 User 模型有 phone 字段且应唯一)
        if User.query.filter_by(phone=phone).first():
            return error_response("该手机号已被注册")

        # 创建新用户 (确保 User 模型支持 phone 字段)
        user = User(username=username, phone=phone)
        user.set_password(password) # 此方法通常处理密码哈希
        db.session.add(user)
        db.session.commit()

        return success_response(message="注册成功")

    except Exception as e:
        # 考虑记录更详细的错误日志 e.g., current_app.logger.error(f"Registration error: {str(e)}")
        return error_response(f"注册失败: {str(e)}")

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return error_response("用户名和密码不能为空")
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return error_response("用户名或密码错误")
        
        # 生成JWT token
        access_token = create_access_token(identity=user.id)
        
        return success_response({
            'token': access_token,
            'user': user.to_dict()
        }, "登录成功")
        
    except Exception as e:
        return error_response(f"登录失败: {str(e)}")
