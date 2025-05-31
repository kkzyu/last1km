import requests
import json
import os
from flask import current_app

class MapService:
    def __init__(self):
        self.amap_key = os.getenv('AMAP_KEY')
        if not self.amap_key:
            raise ValueError("AMAP_KEY not found in environment variables")
    
    def search_places(self, keyword, city="杭州", page_size=10):
        """
        高德地图地点搜索API (输入提示)
        """
        url = "https://restapi.amap.com/v3/assistant/inputtips"
        params = {
            'keywords': keyword,
            'city': city,
            'datatype': 'all',
            'key': self.amap_key,
            'output': 'json'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            current_app.logger.info(f"高德地图搜索响应: {data}")
            
            if data.get('status') == '1':
                results = []
                for tip in data.get('tips', []):
                    # 只处理有具体坐标的地点
                    location = tip.get('location', '')
                    if location and ',' in location:
                        try:
                            lng, lat = location.split(',')
                            result = {
                                'name': tip.get('name'),
                                'address': tip.get('address') or tip.get('district', ''),
                                'location': {
                                    'lat': float(lat),
                                    'lng': float(lng)
                                },
                                'adcode': tip.get('adcode'),
                                'citycode': tip.get('citycode')
                            }
                            results.append(result)
                        except (ValueError, IndexError) as e:
                            current_app.logger.warning(f"解析坐标失败: {location}, 错误: {e}")
                            continue
                
                # 限制返回数量
                results = results[:page_size]
                return {'success': True, 'data': results}
            else:
                error_msg = f"搜索失败: status={data.get('status')}, info={data.get('info')}, infocode={data.get('infocode')}"
                current_app.logger.error(error_msg)
                return {'success': False, 'message': error_msg}
                
        except Exception as e:
            error_msg = f"搜索异常: {str(e)}"
            current_app.logger.error(error_msg)
            return {'success': False, 'message': error_msg}
    
    def calculate_route(self, origin_lat, origin_lng, dest_lat, dest_lng):
        """
        高德地图路线规划API - 骑行路径规划
        """
        url = "https://restapi.amap.com/v4/direction/bicycling"
        params = {
            'origin': f"{origin_lng},{origin_lat}",  # 高德API经纬度顺序为：经度,纬度
            'destination': f"{dest_lng},{dest_lat}",
            'key': self.amap_key,
            'output': 'json'
        }
        
        try:
            current_app.logger.info(f"高德地图路线规划请求: {url}")
            current_app.logger.info(f"请求参数: {params}")
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            current_app.logger.info(f"高德地图路线规划响应: {data}")
            
            # 高德地图V4 API的成功判断条件
            if data.get('errcode') == 0 and data.get('data'):
                route_data = data.get('data', {})
                paths = route_data.get('paths', [])
                
                if paths:
                    path = paths[0]  # 取第一条路径
                    duration = path.get('duration', 0)  # 秒
                    distance = path.get('distance', 0)   # 米
                    
                    try:
                        duration_int = int(float(duration))
                        distance_int = int(float(distance))
                        
                        return {
                            'success': True,
                            'data': {
                                'duration': round(duration_int / 60),  # 转换为分钟
                                'distance': round(distance_int / 1000, 2),  # 转换为公里
                                'mode': '骑行',
                                'route_info': path
                            }
                        }
                    except (ValueError, TypeError) as e:
                        return {'success': False, 'message': f"解析骑行路径数据失败: {e}"}
                else:
                    return {'success': False, 'message': "未找到骑行路径"}
            else:
                # 如果骑行路径规划失败，尝试步行路径规划作为备选
                current_app.logger.warning(f"骑行路径规划失败: errcode={data.get('errcode')}, errmsg={data.get('errmsg')}")
                return self._calculate_walking_route_fallback(origin_lat, origin_lng, dest_lat, dest_lng)
                
        except Exception as e:
            error_msg = f"骑行路径规划异常: {str(e)}"
            current_app.logger.error(error_msg)
            return {'success': False, 'message': error_msg}
    
    def _calculate_walking_route_fallback(self, origin_lat, origin_lng, dest_lat, dest_lng):
        """
        备选方案：使用步行路径规划，然后估算骑行时间
        """
        url = "https://restapi.amap.com/v3/direction/walking"
        params = {
            'origin': f"{origin_lng},{origin_lat}",
            'destination': f"{dest_lng},{dest_lat}",
            'key': self.amap_key,
            'output': 'json'
        }
        
        try:
            current_app.logger.info(f"高德地图步行路径规划请求: {url}")
            current_app.logger.info(f"请求参数: {params}")
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            current_app.logger.info(f"高德地图步行路径规划响应: {data}")
            
            if data.get('status') == '1':
                route_data = data.get('route', {})
                paths = route_data.get('paths', [])
                
                if paths:
                    path = paths[0]  # 取第一条路径
                    duration = path.get('duration', 0)  # 秒
                    distance = path.get('distance', 0)   # 米
                    
                    try:
                        duration_int = int(float(duration))
                        distance_int = int(float(distance))
                        
                        # 假设骑行速度是步行速度的3倍
                        estimated_bike_duration = max(1, round(duration_int / 3 / 60))  # 转换为分钟
                        
                        return {
                            'success': True,
                            'data': {
                                'duration': estimated_bike_duration,
                                'distance': round(distance_int / 1000, 2),  # 转换为公里
                                'mode': '估算骑行',
                                'route_info': path
                            }
                        }
                    except (ValueError, TypeError) as e:
                        return {'success': False, 'message': f"解析步行路径数据失败: {e}"}
                else:
                    return {'success': False, 'message': "未找到步行路径"}
            else:
                error_msg = f"步行路径规划失败: status={data.get('status')}, info={data.get('info')}, infocode={data.get('infocode')}"
                current_app.logger.error(error_msg)
                return {'success': False, 'message': error_msg}
                
        except Exception as e:
            error_msg = f"步行路径规划异常: {str(e)}"
            current_app.logger.error(error_msg)
            return {'success': False, 'message': error_msg}

# 创建全局实例
map_service = MapService()