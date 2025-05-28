from app import create_app
from services.auth_service import AuthService
from models.user import User
from models import db

def test_register_and_login():
    app = create_app('testing')  # 使用测试配置
    
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 清理测试数据
        existing_user = User.query.filter_by(username="testuser123").first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
            print("已删除现有测试用户")
        
        # 测试注册
        print("=== 测试注册 ===")
        success, message, user = AuthService.register_user(
            username="testuser123",
            password="password123",
            nickname="测试用户",
            phone="13800138000",
            email="test@example.com"
        )
        
        print(f"注册结果: {success}, 消息: {message}")
        if user:
            print(f"用户ID: {user.id}, 用户名: {user.username}")
        
        # 测试登录
        print("\n=== 测试登录 ===")
        success, message, user, token = AuthService.login_user("testuser123", "password123")
        
        print(f"登录结果: {success}, 消息: {message}")
        if user:
            print(f"用户ID: {user.id}, 用户名: {user.username}")
            print(f"Token: {token[:50]}..." if token else "无Token")
        
        # 测试错误密码
        print("\n=== 测试错误密码 ===")
        success, message, user, token = AuthService.login_user("testuser123", "wrongpassword")
        print(f"登录结果: {success}, 消息: {message}")
        
        # 清理测试数据
        test_user = User.query.filter_by(username="testuser123").first()
        if test_user:
            db.session.delete(test_user)
            db.session.commit()
            print("\n已清理测试数据")

if __name__ == "__main__":
    test_register_and_login()