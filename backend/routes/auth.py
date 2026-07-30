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
        identity=str(user.id),
        additional_claims={'username': user.username, 'is_admin': user.is_admin}
    )
    return jsonify({
        'token': token,
        'user': {'id': user.id, 'username': user.username, 'is_admin': user.is_admin}
    })


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': '用户名和密码不能为空'}), 400

    username = data['username'].strip()
    password = data['password']

    if len(username) < 2 or len(username) > 20:
        return jsonify({'error': '用户名长度需在2-20个字符之间'}), 400
    if len(password) < 6:
        return jsonify({'error': '密码长度不能少于6位'}), 400

    if User.find_by_username(username):
        return jsonify({'error': '用户名已存在'}), 409

    User.add(username, password)
    return jsonify({'message': '注册成功'}), 201


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
