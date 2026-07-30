from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.bill import Bill

stats_bp = Blueprint('stats', __name__, url_prefix='/api/stats')


@stats_bp.route('/summary', methods=['GET'])
@jwt_required()
def summary():
    uid = int(get_jwt_identity())
    m_inc, m_exp, m_bal = Bill.get_month_data(uid)
    y_inc, y_exp, y_bal = Bill.get_year_data(uid)
    a_inc, a_exp, a_bal = Bill.get_all_data(uid)
    return jsonify({
        'month': {'income': m_inc, 'expense': m_exp, 'balance': m_bal},
        'year': {'income': y_inc, 'expense': y_exp, 'balance': y_bal},
        'all': {'income': a_inc, 'expense': a_exp, 'balance': a_bal}
    })


@stats_bp.route('/12month', methods=['GET'])
@jwt_required()
def month12():
    uid = int(get_jwt_identity())
    return jsonify(Bill.get_12month_data(uid))


@stats_bp.route('/expense-pie', methods=['GET'])
@jwt_required()
def expense_pie():
    uid = int(get_jwt_identity())
    return jsonify(Bill.get_pie_data(uid))


@stats_bp.route('/income-pie', methods=['GET'])
@jwt_required()
def income_pie():
    uid = int(get_jwt_identity())
    return jsonify(Bill.get_income_pie(uid))


@stats_bp.route('/top5', methods=['GET'])
@jwt_required()
def top5():
    uid = int(get_jwt_identity())
    return jsonify(Bill.get_top5_spend(uid))


@stats_bp.route('/7day', methods=['GET'])
@jwt_required()
def day7():
    uid = int(get_jwt_identity())
    return jsonify(Bill.get_7day_data(uid))


@stats_bp.route('/balance-trend', methods=['GET'])
@jwt_required()
def balance_trend():
    uid = int(get_jwt_identity())
    return jsonify(Bill.get_balance_trend(uid))


@stats_bp.route('/recent', methods=['GET'])
@jwt_required()
def recent():
    uid = int(get_jwt_identity())
    bills = Bill.get_home_top10(uid)
    result = []
    for b in bills:
        result.append({
            'bill_date': b.bill_date.strftime('%Y-%m-%d %H:%M:%S') if b.bill_date else '',
            'type': b.type,
            'money': b.money,
            'category': b.category,
            'sub_category': b.sub_category
        })
    return jsonify(result)
