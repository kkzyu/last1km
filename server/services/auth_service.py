import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from models import db
from models.user import User

class AuthService:
    @staticmethod
    def register_user(username, password, nickname=None, phone=None, email=None, gender=None):
        """用户注册服务"""
        try:
            current_app.logger.info(f"开始注册用户: {username}")
            
            # 验证用户名格式
            is_valid, msg = User.validate_username(username)
            if not is_valid:
                current_app.logger.warning(f"用户名验证失败: {msg}")
                return False, msg, None
            
            # 检查用户名是否已存在
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                current_app.logger.warning(f"用户名已存在: {username}")
                return False, "用户名已存在", None
            
            # 验证手机号
            if phone:
                is_valid, msg = User.validate_phone(phone)
                if not is_valid:
                    current_app.logger.warning(f"手机号验证失败: {msg}")
                    return False, msg, None
                
                existing_phone = User.query.filter_by(phone=phone).first()
                if existing_phone:
                    current_app.logger.warning(f"手机号已被注册: {phone}")
                    return False, "手机号已被注册", None
            
            # 验证邮箱
            if email:
                is_valid, msg = User.validate_email(email)
                if not is_valid:
                    current_app.logger.warning(f"邮箱验证失败: {msg}")
                    return False, msg, None
                
                existing_email = User.query.filter_by(email=email).first()
                if existing_email:
                    current_app.logger.warning(f"邮箱已被注册: {email}")
                    return False, "邮箱已被注册", None
            
            # 创建新用户 - 只使用存在的字段
            user = User(
                username=username,
                nickname=nickname or username,
                phone=phone,
                email=email,
                gender=gender,
                default_pickup_address='',
                default_delivery_address=''
            )
            user.set_password(password)
            current_app.logger.info(f"创建用户对象成功: {username}")
            
            db.session.add(user)
            db.session.commit()
            current_app.logger.info(f"用户注册成功: {username}, ID: {user.id}")
            
            return True, "注册成功", user
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"注册用户失败: {str(e)}")
            return False, f"注册失败: {str(e)}", None
    
    @staticmethod
    def login_user(username, password):
        """用户登录服务"""
        try:
            current_app.logger.info(f"尝试登录用户: {username}")
            
            # 查找用户
            user = User.query.filter_by(username=username).first()
            if not user:
                current_app.logger.warning(f"用户不存在: {username}")
                return False, "用户名不存在", None, None
            
            current_app.logger.info(f"找到用户: {username}, ID: {user.id}")
            
            # 验证密码
            if not user.check_password(password):
                current_app.logger.warning(f"密码错误: {username}")
                return False, "密码错误", None, None
            
            current_app.logger.info(f"密码验证成功: {username}")
            
            # 检查用户状态
            if user.status != 'active':
                current_app.logger.warning(f"用户账户被禁用: {username}")
                return False, "账户已被禁用", None, None
            
            # 生成token
            token = AuthService.generate_token(user.id)
            if not token:
                current_app.logger.error(f"生成token失败: {username}")
                return False, "登录失败", None, None
            
            # 更新最后登录时间
            user.update_last_login()
            current_app.logger.info(f"用户登录成功: {username}")
            
            return True, "登录成功", user, token
            
        except Exception as e:
            current_app.logger.error(f"登录失败: {str(e)}")
            return False, f"登录失败: {str(e)}", None, None
    
    @staticmethod
    def generate_token(user_id):
        """生成JWT token"""
        try:
            payload = {
                'sub': user_id,
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
            }
            
            token = jwt.encode(
                payload,
                current_app.config['JWT_SECRET_KEY'],
                algorithm=current_app.config['JWT_ALGORITHM']
            )
            
            current_app.logger.info(f"Token生成成功 for user_id: {user_id}")
            return token
            
        except Exception as e:
            current_app.logger.error(f"生成token失败: {str(e)}")
            return None
    
    @staticmethod
    def verify_token(token):
        """验证JWT token"""
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=[current_app.config['JWT_ALGORITHM']]
            )
            
            user_id = payload['sub']
            user = User.query.get(user_id)
            
            if user and user.status == 'active':
                return user
            
            return None
            
        except jwt.ExpiredSignatureError:
            current_app.logger.warning("Token已过期")
            return None
        except jwt.InvalidTokenError as e:
            current_app.logger.warning(f"Token无效: {str(e)}")
            return None
        except Exception as e:
            current_app.logger.error(f"验证token失败: {str(e)}")
            return None