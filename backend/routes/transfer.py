from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.bill import Bill

transfer_bp = Blueprint('transfer', __name__, url_prefix='/api/transfer')


@transfer_bp.route('', methods=['POST'])
@jwt_required()
def do_transfer():
    uid = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return jsonify({'error': '请求体不能为空'}), 400

    required = ['date', 'out_account', 'in_account', 'money']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} 不能为空'}), 400

    if data['out_account'] == data['in_account']:
        return jsonify({'error': '转出账户和转入账户不能相同'}), 400

    remark = data.get('remark', '')
    # 转出：记为支出
    Bill.add(uid, data['date'], '支出', data['money'], '转账', '转账',
             data['out_account'], '日常账本', 0, remark)
    # 转入：记为收入
    Bill.add(uid, data['date'], '收入', data['money'], '转账', '转账',
             data['in_account'], '日常账本', 0, remark)

    return jsonify({'message': '转账成功'}), 201
