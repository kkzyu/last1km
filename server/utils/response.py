from flask import jsonify

def success_response(data=None, message="操作成功", code=200):
    """成功响应"""
    response = {
        'code': code,
        'message': message,
        'success': True
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), code

def error_response(message="操作失败", code=400, data=None):
    """错误响应"""
    response = {
        'code': code,
        'message': message,
        'success': False
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), code
