from functools import wraps
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models.user import User

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if not claims.get('is_admin'):
            return jsonify({'error': '需要管理员权限'}), 403
        return fn(*args, **kwargs)
    return wrapper


@users_bp.route('', methods=['GET'])
@admin_required
def get_users():
    users = User.get_all()
    return jsonify([{'id': u[0], 'username': u[1], 'is_admin': u[2]} for u in users])


@users_bp.route('', methods=['POST'])
@admin_required
def add_user():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': '用户名和密码不能为空'}), 400
    try:
        User.add(data['username'], data['password'])
    except Exception:
        return jsonify({'error': '用户名已存在'}), 409
    return jsonify({'message': '添加成功'}), 201


@users_bp.route('/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': '用户名和密码不能为空'}), 400
    User.update(user_id, data['username'], data['password'])
    return jsonify({'message': '更新成功'})


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    uid = int(get_jwt_identity())
    if user_id == uid:
        return jsonify({'error': '不能删除自己'}), 400
    User.delete(user_id)
    return jsonify({'message': '删除成功'})
