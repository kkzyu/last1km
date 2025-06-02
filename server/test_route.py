import requests
import os
import json
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
            print(f"路径steps数量: {len(path.get('steps', []))}")
            
            # 打印路径详细信息用于调试
            steps = path.get('steps', [])
            if steps:
                print(f"第一个step的keys: {list(steps[0].keys())}")
                if 'path' in steps[0]:
                    print(f"第一个step的路径点数量: {len(steps[0].get('path', []))}")
                    if steps[0].get('path'):
                        print(f"第一个路径点: {steps[0]['path'][0]}")
                        print(f"路径点类型: {type(steps[0]['path'][0])}")
                else:
                    print("第一个step中没有'path'字段")
                    print(f"第一个step内容: {json.dumps(steps[0], indent=2, ensure_ascii=False)}")
            
            # 保存完整的路径信息到文件用于分析
            with open('route_debug.json', 'w', encoding='utf-8') as f:
                json.dump(path, f, indent=2, ensure_ascii=False)
            print("完整路径信息已保存到 route_debug.json")
            
            return {
                'success': True,
                'data': {
                    'duration': duration_minutes,
                    'distance': distance_km,
                    'mode': '骑行',
                    'route_info': path  # 包含完整路径信息
                }
            }
        else:
            print("❌ 未找到路径")
            return {'success': False, 'message': "未找到路径"}
    else:
        print(f"❌ API调用失败: errcode={data.get('errcode')}, errmsg={data.get('errmsg')}")
        return {'success': False, 'message': "API调用失败"}

if __name__ == "__main__":
    result = test_route_parsing()
    print(f"最终结果: {result}")
