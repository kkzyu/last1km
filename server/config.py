import os
from datetime import timedelta

class Config:
    # 数据库配置
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'last1km-jwt-secret-key-2024'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)  # token有效期7天
    JWT_ALGORITHM = 'HS256'
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    
    # 其他配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'last1km-secret-key-2024'
    
    # CORS配置
    CORS_ORIGINS = ['http://localhost:5173', 'http://127.0.0.1:5173']