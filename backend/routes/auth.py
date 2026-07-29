from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': '用户名和密码不能为空'}), 400

    user = User.login(data['username'], data['password'])
    if not user:
        return jsonify({'error': '用户名或密码错误'}), 401

    token = create_access_token(
        identity=str(user[0]),
        additional_claims={'username': user[1], 'is_admin': user[2]}
    )
    return jsonify({
        'token': token,
        'user': {'id': user[0], 'username': user[1], 'is_admin': user[2]}
    })


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    uid = int(get_jwt_identity())
    claims = get_jwt()
    return jsonify({
        'id': uid,
        'username': claims['username'],
        'is_admin': claims['is_admin']
    })
