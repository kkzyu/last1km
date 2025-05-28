from flask import Blueprint, request, jsonify, current_app
from functools import wraps
from werkzeug.utils import secure_filename
import os
import uuid
from services.auth_service import AuthService
from models.user import User
from utils.auth_helpers import token_required
from models import db
from flask_cors import cross_origin

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
@cross_origin()
def register():
    """用户注册"""
    if request.method == 'OPTIONS':
        return jsonify({'code': 200, 'message': 'OK'}), 200
    try:
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'message': '请求数据不能为空'}), 400
        
        # 验证必填字段
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({'code': 400, 'message': '用户名和密码不能为空'}), 400
        
        # 验证密码长度
        if len(password) < 6:
            return jsonify({'code': 400, 'message': '密码长度不能少于6位'}), 400
        
        # 获取可选字段
        nickname = data.get('nickname', '').strip()
        phone = data.get('phone', '').strip()
        email = data.get('email', '').strip()
        gender = data.get('gender', '').strip()
        
        # 调用注册服务
        success, message, user = AuthService.register_user(
            username=username,
            password=password,
            nickname=nickname,
            phone=phone,
            email=email,
            gender=gender
        )
        
        if success:
            return jsonify({
                'code': 200,
                'message': message,
                'data': {
                    'user': user.to_dict()
                }
            }), 200
        else:
            return jsonify({'code': 400, 'message': message}), 400
        
    except Exception as e:
        current_app.logger.error(f"注册异常: {str(e)}")
        return jsonify({'code': 500, 'message': f'注册失败: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin()
def login():
    """用户登录"""
    if request.method == 'OPTIONS':
        return jsonify({'code': 200, 'message': 'OK'}), 200
    try:
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'message': '请求数据不能为空'}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({'code': 400, 'message': '用户名和密码不能为空'}), 400
        
        # 调用登录服务
        success, message, user, token = AuthService.login_user(username, password)
        
        if success:
            return jsonify({
                'code': 200,
                'message': message,
                'data': {
                    'access_token': token,
                    'user': user.to_dict()
                }
            }), 200
        else:
            return jsonify({'code': 400, 'message': message}), 400
        
    except Exception as e:
        current_app.logger.error(f"登录异常: {str(e)}")
        return jsonify({'code': 500, 'message': f'登录失败: {str(e)}'}), 500

@auth_bp.route('/profile', methods=['GET', 'PUT', 'OPTIONS'])
@cross_origin()
@token_required
def profile_handler(current_user):
    """处理用户资料的获取和更新"""
    if request.method == 'OPTIONS':
        return jsonify({'code': 200, 'message': 'OK'}), 200
    elif request.method == 'GET':
        return get_profile(current_user)
    elif request.method == 'PUT':
        return update_profile(current_user)
    
def get_profile(current_user):
    """获取用户信息"""
    try:
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': {
                'user': current_user.to_dict()
            }
        }), 200
    except Exception as e:
        current_app.logger.error(f"获取用户信息异常: {str(e)}")
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500


def update_profile(current_user):
    """更新用户信息"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'message': '请求数据不能为空'}), 400
        
        # 可更新的字段
        updatable_fields = ['nickname', 'gender', 'default_pickup_address', 'default_delivery_address', 'avatar']
        
        for field in updatable_fields:
            if field in data:
                setattr(current_user, field, data[field])
        
        # 特殊处理手机号和邮箱
        if 'phone' in data:
            phone = data['phone'].strip()
            if phone:
                is_valid, msg = User.validate_phone(phone)
                if not is_valid:
                    return jsonify({'code': 400, 'message': msg}), 400
                # 检查是否已被其他用户使用
                existing = User.query.filter(User.phone == phone, User.id != current_user.id).first()
                if existing:
                    return jsonify({'code': 400, 'message': '手机号已被其他用户使用'}), 400
            current_user.phone = phone
        
        if 'email' in data:
            email = data['email'].strip()
            if email:
                is_valid, msg = User.validate_email(email)
                if not is_valid:
                    return jsonify({'code': 400, 'message': msg}), 400
                # 检查是否已被其他用户使用
                existing = User.query.filter(User.email == email, User.id != current_user.id).first()
                if existing:
                    return jsonify({'code': 400, 'message': '邮箱已被其他用户使用'}), 400
            current_user.email = email
        
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '更新成功',
            'data': {
                'user': current_user.to_dict()
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"更新用户信息异常: {str(e)}")
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500
    
@auth_bp.route('/logout', methods=['POST'])
@token_required
@cross_origin()
def logout(current_user):
    """用户登出"""
    return jsonify({
        'code': 200,
        'message': '登出成功'
    }), 200


@auth_bp.route('/change-password', methods=['POST'])
@token_required
@cross_origin()
def change_password(current_user):
    """修改密码"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'message': '请求数据不能为空'}), 400
        
        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')
        
        if not old_password or not new_password:
            return jsonify({'code': 400, 'message': '原密码和新密码不能为空'}), 400
        
        if not current_user.check_password(old_password):
            return jsonify({'code': 400, 'message': '原密码错误'}), 400
        
        if len(new_password) < 6:
            return jsonify({'code': 400, 'message': '新密码长度不能少于6位'}), 400
        
        current_user.set_password(new_password)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '密码修改成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"修改密码异常: {str(e)}")
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500

@auth_bp.route('/verify-token', methods=['POST'])
@token_required
@cross_origin()
def verify_token(current_user):
    """验证token有效性"""
    return jsonify({
        'code': 200,
        'message': 'Token有效',
        'data': {
            'user': current_user.to_dict()
        }
    }), 200

@auth_bp.route('/upload-avatar', methods=['POST'])
@token_required
@cross_origin()
def upload_avatar(current_user):
    """上传头像"""
    try:
        if 'avatar' not in request.files:
            return jsonify({'code': 400, 'message': '没有选择文件'}), 400
        
        file = request.files['avatar']
        if file.filename == '':
            return jsonify({'code': 400, 'message': '没有选择文件'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'code': 400, 'message': '不支持的文件格式，请上传png、jpg、jpeg或gif格式的图片'}), 400
        
        # 创建上传目录
        upload_folder = os.path.join(current_app.root_path, 'static', 'avatars')
        os.makedirs(upload_folder, exist_ok=True)
        
        # 生成唯一文件名
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{file_extension}"
        file_path = os.path.join(upload_folder, filename)
        
        # 保存文件
        file.save(file_path)
        
        # 生成访问URL
        avatar_url = f"/static/avatars/{filename}"
        
        # 更新用户头像
        current_user.avatar = avatar_url
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '头像上传成功',
            'data': {
                'avatar_url': avatar_url
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"上传头像异常: {str(e)}")
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500
        