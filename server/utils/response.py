from flask import jsonify

def success_response(data=None, message="操作成功", status_code=200):
    """成功响应格式化"""
    response_data = {
        'success': True,
        'message': message
    }
    
    if data is not None:
        response_data['data'] = data
    
    response = jsonify(response_data)
    response.status_code = status_code
    return response

def error_response(message="操作失败", status_code=400, error_code=None):
    """错误响应格式化"""
    response_data = {
        'success': False,
        'message': message
    }
    
    if error_code:
        response_data['error_code'] = error_code
    
    response = jsonify(response_data)
    response.status_code = status_code
    return response

def paginated_response(items, pagination, message="获取成功"):
    """分页响应格式化"""
    return success_response({
        'items': items,
        'pagination': {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }, message)
