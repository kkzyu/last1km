import requests
import json

BASE_URL = 'http://localhost:5000/api/auth'

def test_full_auth_flow():
    """测试完整的认证流程"""
    
    # 测试数据
    test_user = {
        "username": "apitest123",
        "password": "password123",
        "nickname": "API测试用户",
        "phone": "13912345678",
        "email": "apitest@example.com"
    }
    
    print("=== 完整API测试开始 ===\n")
    
    # 1. 测试注册
    print("1. 测试注册")
    try:
        response = requests.post(f"{BASE_URL}/register", json=test_user)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get('code') != 200:
            print("注册失败，停止测试")
            return
            
    except Exception as e:
        print(f"注册请求失败: {e}")
        return
    
    print("\n" + "="*50 + "\n")
    
    # 2. 测试登录
    print("2. 测试登录")
    try:
        login_data = {
            "username": test_user["username"],
            "password": test_user["password"]
        }
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get('code') != 200:
            print("登录失败，停止测试")
            return
            
        token = result['data']['token']
        print(f"\n获取到Token: {token[:50]}...")
        
    except Exception as e:
        print(f"登录请求失败: {e}")
        return
    
    print("\n" + "="*50 + "\n")
    
    # 3. 测试获取用户信息
    print("3. 测试获取用户信息")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/profile", headers=headers)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
    except Exception as e:
        print(f"获取用户信息失败: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 4. 测试更新用户信息
    print("4. 测试更新用户信息")
    try:
        update_data = {
            "nickname": "更新后的昵称",
            "gender": "male",
            "school_info": "测试大学"
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{BASE_URL}/profile", json=update_data, headers=headers)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
    except Exception as e:
        print(f"更新用户信息失败: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 5. 测试验证token
    print("5. 测试验证token")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/verify-token", headers=headers)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
    except Exception as e:
        print(f"验证token失败: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 6. 测试登出
    print("6. 测试登出")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/logout", headers=headers)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
    except Exception as e:
        print(f"登出失败: {e}")
    
    print("\n=== API测试完成 ===")

if __name__ == "__main__":
    test_full_auth_flow()