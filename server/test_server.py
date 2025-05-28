import requests
import json

def test_server():
    """测试服务器是否正常运行"""
    base_url = "http://localhost:5000"
    
    try:
        # 测试注册接口
        register_data = {
            "username": "testuser123",
            "password": "123456",
            "nickname": "测试用户"
        }
        
        print("测试注册接口...")
        response = requests.post(f"{base_url}/api/auth/register", 
                               json=register_data,
                               headers={'Content-Type': 'application/json'})
        
        print(f"注册响应状态码: {response.status_code}")
        print(f"注册响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 注册接口正常")
        else:
            print("❌ 注册接口异常")
            
    except Exception as e:
        print(f"❌ 服务器连接失败: {e}")
        print("请确保后端服务正在运行")

if __name__ == '__main__':
    test_server()