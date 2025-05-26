from flask import Flask, Response, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from models.user import User
from models.order import Order  
from models.deliverer import Deliverer
from models.address import Address
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 配置 CORS
    CORS(app, 
         origins=["http://localhost:3000"],
         allow_credentials=True,
         supports_credentials=True,
         resources={
             r"/api/*": {
                 "origins": ["http://localhost:3000"],
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                 "allow_headers": ["Content-Type", "Authorization", "Accept"],
                 "expose_headers": ["Authorization"],
                 "max_age": 120
             }
         })
    
    # 初始化数据库
    db.init_app(app)
    
    # 初始化 JWT
    jwt = JWTManager(app)
    
    # 注册路由蓝图
    from routes.auth import auth_bp
    from routes.orders import orders_bp
    from routes.users import users_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
        
        # 创建测试用户和配送员
        if not User.query.first():
            test_user = User(username='testuser', nickname='测试用户')
            test_user.set_password('123456')
            db.session.add(test_user)
            
            test_deliverer = Deliverer(name='张三', phone='13800138000')
            db.session.add(test_deliverer)
            
            db.session.commit()
            print("已创建测试数据")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
