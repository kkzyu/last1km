from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 配置 CORS
    CORS(app, 
         origins=['http://localhost:5173', 'http://127.0.0.1:5173'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization'],
         supports_credentials=True
    )
    
    # 初始化数据库
    db.init_app(app)
    
    # 注册蓝图
    from routes.auth import auth_bp
    from routes.address import address_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(address_bp)
    
    # 添加根路由用于测试
    @app.route('/')
    def index():
        return jsonify({
            'code': 200,
            'message': 'Last1km API Server is running!',
            'version': '1.0.0'
        })
    
    # 添加健康检查路由
    @app.route('/health')
    def health_check():
        return jsonify({
            'code': 200,
            'message': 'Server is healthy',
            'status': 'OK'
        })
    
    # 配置日志
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/last1km.log',
                                         maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Last1km startup')
    
    if app.config.get('TESTING', False) or app.config.get('DEBUG', True):
        from routes.test_data import test_data_bp
        app.register_blueprint(test_data_bp, url_prefix='/api/test')

    # 创建数据库表
    with app.app_context():
        try:
            db.create_all()
            print("✓ 数据库表创建成功")
        except Exception as e:
            print(f"❌ 数据库表创建失败: {e}")
    
    return app

def print_routes(app):
    """打印所有注册的路由"""
    print("\n注册的路由:")
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods - {'HEAD', 'OPTIONS'})
        print(f"  {rule.endpoint:30s} {methods:20s} {rule.rule}")
    print()

if __name__ == '__main__':
    app = create_app()
    
    # 打印路由信息用于调试
    print_routes(app)
    
    print("🚀 启动 Last1km 后端服务...")
    print("📍 访问地址: http://localhost:5000")
    print("📊 健康检查: http://localhost:5000/health")
    print("🔧 API文档: http://localhost:5000/api/auth/register")
    
    app.run(host='0.0.0.0', port=5000, debug=True)