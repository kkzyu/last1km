from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from utils.response import success_response, error_response

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return error_response("用户名和密码不能为空")
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return error_response("用户名已存在")
        
        # 创建新用户
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return success_response(message="注册成功")
        
    except Exception as e:
        return error_response(f"注册失败: {str(e)}")

@auth_bp.route('/login', methods=['POST'])
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
