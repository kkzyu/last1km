from flask import Blueprint, request
from services.map_service import map_service
from utils.response import success_response, error_response
from utils.auth_helpers import token_required

map_bp = Blueprint('map', __name__)

@map_bp.route('/search', methods=['POST'])
@token_required
def search_places(current_user):
    """地点搜索"""
    try:
        data = request.get_json()
        keyword = data.get('keyword', '').strip()
        city = data.get('city', '杭州')
        
        if not keyword:
            return error_response("搜索关键词不能为空")
        
        result = map_service.search_places(keyword, city)
        
        if result['success']:
            return success_response(result['data'])
        else:
            return error_response(result['message'])
            
    except Exception as e:
        return error_response(f"搜索失败: {str(e)}")

@map_bp.route('/route', methods=['POST'])
@token_required
def calculate_route(current_user):
    """路线规划"""
    try:
        data = request.get_json()
        origin = data.get('origin', {})
        destination = data.get('destination', {})
        
        if not all([origin.get('lat'), origin.get('lng'), 
                   destination.get('lat'), destination.get('lng')]):
            return error_response("起点和终点坐标不能为空")
        
        result = map_service.calculate_route(
            origin['lat'], origin['lng'],
            destination['lat'], destination['lng']
        )
        
        if result['success']:
            return success_response(result['data'])
        else:
            return error_response(result['message'])
            
    except Exception as e:
        return error_response(f"路线规划失败: {str(e)}")

@map_bp.route('/config', methods=['GET'])
def get_map_config():
    """获取前端地图配置（无需认证）"""
    try:
        config = map_service.get_frontend_map_config()
        return success_response(config)
    except Exception as e:
        return error_response(f"获取地图配置失败: {str(e)}")