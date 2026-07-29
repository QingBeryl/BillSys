from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.bill import Bill

bills_bp = Blueprint('bills', __name__, url_prefix='/api/bills')


def serialize_bill(row):
    """将数据库行转为可JSON序列化的字典"""
    return {
        'id': row[0],
        'user_id': row[1],
        'bill_date': row[2].strftime('%Y-%m-%d %H:%M:%S') if hasattr(row[2], 'strftime') else str(row[2]),
        'type': row[3],
        'money': float(row[4]),
        'category': row[5],
        'sub_category': row[6],
        'account': row[7],
        'book_name': row[8] if len(row) > 8 else '日常账本',
        'refund': float(row[9]) if len(row) > 9 and row[9] else 0,
        'remark': row[10] if len(row) > 10 else ''
    }


@bills_bp.route('', methods=['GET'])
@jwt_required()
def get_bills():
    uid = int(get_jwt_identity())
    bills = Bill.get_by_user(uid)
    return jsonify([serialize_bill(b) for b in bills])


@bills_bp.route('/<int:bill_id>', methods=['GET'])
@jwt_required()
def get_bill(bill_id):
    uid = int(get_jwt_identity())
    bill = Bill.get_by_id(bill_id, uid)
    if not bill:
        return jsonify({'error': '账单不存在'}), 404
    return jsonify(serialize_bill(bill))


@bills_bp.route('', methods=['POST'])
@jwt_required()
def add_bill():
    uid = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return jsonify({'error': '请求体不能为空'}), 400

    required = ['bill_date', 'type', 'money', 'category', 'sub_category', 'account']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} 不能为空'}), 400

    Bill.add(
        uid,
        data['bill_date'],
        data['type'],
        data['money'],
        data['category'],
        data['sub_category'],
        data['account'],
        data.get('book_name', '日常账本'),
        data.get('refund', 0),
        data.get('remark', '')
    )
    return jsonify({'message': '添加成功'}), 201


@bills_bp.route('/<int:bill_id>', methods=['PUT'])
@jwt_required()
def update_bill(bill_id):
    uid = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return jsonify({'error': '请求体不能为空'}), 400

    Bill.update(
        bill_id, uid,
        data.get('bill_date'),
        data.get('type'),
        data.get('money'),
        data.get('category'),
        data.get('sub_category'),
        data.get('account'),
        data.get('book_name', '日常账本'),
        data.get('refund', 0),
        data.get('remark', '')
    )
    return jsonify({'message': '更新成功'})


@bills_bp.route('/<int:bill_id>', methods=['DELETE'])
@jwt_required()
def delete_bill(bill_id):
    uid = int(get_jwt_identity())
    Bill.delete(bill_id, uid)
    return jsonify({'message': '删除成功'})


@bills_bp.route('/query', methods=['POST'])
@jwt_required()
def query_bills():
    uid = int(get_jwt_identity())
    data = request.get_json() or {}
    results = Bill.get_by_query(
        uid,
        data.get('start'),
        data.get('end'),
        data.get('type'),
        data.get('category'),
        data.get('sub_category'),
        data.get('account'),
        data.get('min'),
        data.get('max')
    )
    return jsonify([serialize_bill(b) for b in results])
