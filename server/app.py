from flask import Flask, Response, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from models.user import User
from models.order import Order  
from models.deliverer import Deliverer
from models.address import Address
from models.chat_message import ChatMessage  # 添加这行
import os
import traceback

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    upload_folder = app.config.get('UPLOAD_FOLDER')
    if upload_folder and not os.path.exists(upload_folder):
        os.makedirs(upload_folder, exist_ok=True)
    
    # 配置 CORS
    CORS(app, 
         origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         expose_headers=["Authorization"])

    # 添加全局错误处理器以确保所有响应都有CORS头
    @app.after_request
    def after_request(response):
        origin = request.headers.get('Origin')
        if origin in ['http://localhost:3000', 'http://localhost:3001','http://localhost:3002']:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Accept, Origin, X-Requested-With'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    # 添加一个简单的OPTIONS处理器，确保所有路由都支持OPTIONS
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = Response()
            origin = request.headers.get('Origin')
            if origin in ['http://localhost:3000', 'http://localhost:3001', 'http://localhost:3002']:
                response.headers['Access-Control-Allow-Origin'] = origin
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Accept, Origin, X-Requested-With'
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                response.headers['Access-Control-Allow-Credentials'] = 'true'
            return response

    # 全局错误处理器，确保所有错误响应都有CORS头
    @app.errorhandler(500)
    def handle_500(e):
        app.logger.error(f"Internal Server Error: {str(e)}")
        app.logger.error(f"Traceback: {traceback.format_exc()}")
        response = jsonify({
            'success': False,
            'message': '服务器内部错误',
            'error': str(e) if app.debug else '服务器内部错误'
        })
        response.status_code = 500
        return response

    @app.errorhandler(404)
    def handle_404(e):
        response = jsonify({
            'success': False,
            'message': '请求的资源不存在',
        })
        response.status_code = 404
        return response
    
    # 初始化数据库
    db.init_app(app)
    
    # 初始化 JWT
    jwt = JWTManager(app)
    
    # 注册路由蓝图
    from routes.auth import auth_bp
    from routes.orders import orders_bp
    from routes.users import users_bp
    from routes.map import map_bp
    from routes.faq import faq_bp
    from routes.chat import chat_bp  # 导入聊天路由
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(map_bp, url_prefix='/api/map')
    app.register_blueprint(faq_bp, url_prefix='/api/faq')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')  # 注册聊天路由

    @app.route('/static/uploads/<filename>')
    def uploaded_file(filename):
        upload_folder = app.config.get('UPLOAD_FOLDER')
        return send_from_directory(upload_folder, filename)
    
    # 添加调试路由
    @app.route('/debug/routes')
    def debug_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods),
                'rule': str(rule)
            })
        return {'routes': routes}
    
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
