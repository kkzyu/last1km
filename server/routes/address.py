from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
from models.address import Address
from models.user import User
from utils.auth_helpers import token_required
from models import db

address_bp = Blueprint('address', __name__, url_prefix='/api/address')

@address_bp.route('/list', methods=['GET', 'OPTIONS'])
@cross_origin()
@token_required
def get_addresses(current_user):
    """获取用户地址列表"""
    if request.method == 'OPTIONS':
        return jsonify({'code': 200, 'message': 'OK'}), 200
        
    try:
        # 获取查询参数
        address_type = request.args.get('type')  # pickup 或 delivery
        
        query = Address.query.filter_by(user_id=current_user.id)
        if address_type:
            query = query.filter_by(address_type=address_type)
        
        addresses = query.order_by(Address.is_default.desc(), Address.updated_at.desc()).all()
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': [addr.to_dict() for addr in addresses]
        }), 200
    except Exception as e:
        current_app.logger.error(f"获取地址列表异常: {str(e)}")
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500

@address_bp.route('/add', methods=['POST', 'OPTIONS'])
@cross_origin()
@token_required
def add_address(current_user):
    """添加地址"""
    if request.method == 'OPTIONS':
        return jsonify({'code': 200, 'message': 'OK'}), 200
        
    try:
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'message': '请求数据不能为空'}), 400
        
        # 验证必填字段
        required_fields = ['address_type', 'name', 'address_detail']
        for field in required_fields:
            if not data.get(field, '').strip():
                return jsonify({'code': 400, 'message': f'{field}不能为空'}), 400
        
        # 验证地址类型
        if data['address_type'] not in ['pickup', 'delivery']:
            return jsonify({'code': 400, 'message': '地址类型无效'}), 400
        
        # 如果设置为默认地址，先取消该类型的其他默认地址
        if data.get('is_default', False):
            Address.query.filter_by(
                user_id=current_user.id,
                address_type=data['address_type'],
                is_default=True
            ).update({'is_default': False})
        
        # 创建新地址
        address = Address(
            user_id=current_user.id,
            address_type=data['address_type'],
            name=data['name'].strip(),
            address_detail=data['address_detail'].strip(),
            contact_person=data.get('contact_person', '').strip(),
            contact_phone=data.get('contact_phone', '').strip(),
            notes=data.get('notes', '').strip(),
            is_default=data.get('is_default', False)
        )
        
        db.session.add(address)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '添加成功',
            'data': address.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"添加地址异常: {str(e)}")
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500

@address_bp.route('/update/<int:address_id>', methods=['PUT', 'OPTIONS'])
@cross_origin()
@token_required
def update_address(current_user, address_id):
    """更新地址"""
    if request.method == 'OPTIONS':
        return jsonify({'code': 200, 'message': 'OK'}), 200
        
    try:
        address = Address.query.filter_by(id=address_id, user_id=current_user.id).first()
        if not address:
            return jsonify({'code': 404, 'message': '地址不存在'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'message': '请求数据不能为空'}), 400
        
        # 如果设置为默认地址，先取消该类型的其他默认地址
        if data.get('is_default', False) and not address.is_default:
            Address.query.filter_by(
                user_id=current_user.id,
                address_type=address.address_type,
                is_default=True
            ).update({'is_default': False})
        
        # 更新字段
        updatable_fields = ['name', 'address_detail', 'contact_person', 'contact_phone', 'notes', 'is_default']
        for field in updatable_fields:
            if field in data:
                if field in ['name', 'address_detail', 'contact_person', 'contact_phone', 'notes']:
                    setattr(address, field, data[field].strip() if data[field] else '')
                else:
                    setattr(address, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '更新成功',
            'data': address.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"更新地址异常: {str(e)}")
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500

@address_bp.route('/delete/<int:address_id>', methods=['DELETE', 'OPTIONS'])
@cross_origin()
@token_required
def delete_address(current_user, address_id):
    """删除地址"""
    if request.method == 'OPTIONS':
        return jsonify({'code': 200, 'message': 'OK'}), 200
        
    try:
        address = Address.query.filter_by(id=address_id, user_id=current_user.id).first()
        if not address:
            return jsonify({'code': 404, 'message': '地址不存在'}), 404
        
        db.session.delete(address)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '删除成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"删除地址异常: {str(e)}")
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500

@address_bp.route('/default', methods=['GET', 'OPTIONS'])
@cross_origin()
@token_required
def get_default_addresses(current_user):
    """获取默认地址"""
    if request.method == 'OPTIONS':
        return jsonify({'code': 200, 'message': 'OK'}), 200
        
    try:
        pickup_address = Address.query.filter_by(
            user_id=current_user.id,
            address_type='pickup',
            is_default=True
        ).first()
        
        delivery_address = Address.query.filter_by(
            user_id=current_user.id,
            address_type='delivery',
            is_default=True
        ).first()
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': {
                'pickup_address': pickup_address.to_dict() if pickup_address else None,
                'delivery_address': delivery_address.to_dict() if delivery_address else None
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"获取默认地址异常: {str(e)}")
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500