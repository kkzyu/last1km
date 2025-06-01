import requests
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_route_parsing():
    """测试路线规划API数据解析"""
    amap_key = os.getenv('AMAP_KEY')
    
    # 使用固定的杭州坐标进行测试
    origin_lng, origin_lat = "120.219375", "30.259244"  # 浙大紫金港
    dest_lng, dest_lat = "120.131441", "30.279401"     # 西湖
    
    url = "https://restapi.amap.com/v4/direction/bicycling"
    params = {
        'origin': f"{origin_lng},{origin_lat}",
        'destination': f"{dest_lng},{dest_lat}",
        'key': amap_key,
        'output': 'json'
    }
    
    print("=== 测试路线规划数据解析 ===")
    
    response = requests.get(url, params=params)
    data = response.json()
    
    print(f"原始响应状态码: {response.status_code}")
    print(f"errcode: {data.get('errcode')}")
    print(f"errmsg: {data.get('errmsg')}")
    
    # 使用修复后的逻辑解析数据
    if data.get('errcode') == 0 and data.get('data'):
        route_data = data.get('data', {})
        paths = route_data.get('paths', [])
        
        if paths:
            path = paths[0]
            duration = path.get('duration', 0)  # 秒
            distance = path.get('distance', 0)   # 米
            
            duration_minutes = round(int(duration) / 60)
            distance_km = round(int(distance) / 1000, 2)
            
            print(f"✅ 解析成功!")
            print(f"路线时长: {duration} 秒 -> {duration_minutes} 分钟")
            print(f"路线距离: {distance} 米 -> {distance_km} 公里")
            
            return {
                'success': True,
                'data': {
                    'duration': duration_minutes,
                    'distance': distance_km,
                    'mode': '骑行'
                }
            }
        else:
            print("❌ 未找到路径")
            return {'success': False, 'message': "未找到路径"}
    else:
        print(f"❌ API请求失败: errcode={data.get('errcode')}, errmsg={data.get('errmsg')}")
        return {'success': False, 'message': f"API请求失败: {data.get('errmsg')}"}

if __name__ == "__main__":
    result = test_route_parsing()
    print(f"\n最终结果: {result}")