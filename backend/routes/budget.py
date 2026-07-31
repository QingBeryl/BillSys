from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.budget import Budget
from models.bill import Bill
from datetime import datetime

budget_bp = Blueprint('budget', __name__, url_prefix='/api/budget')


@budget_bp.route('', methods=['GET'])
@jwt_required()
def get_budgets():
    """获取某月的所有预算设置"""
    uid = int(get_jwt_identity())
    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    budgets = Budget.get_by_month(uid, month)
    return jsonify([b.to_dict() for b in budgets])


@budget_bp.route('', methods=['POST'])
@jwt_required()
def set_budget():
    """设置/更新某月某分类的预算"""
    uid = int(get_jwt_identity())
    data = request.get_json() or {}
    month = data.get('month', datetime.now().strftime('%Y-%m'))
    category = data.get('category', 'total')
    amount = data.get('amount', 0)

    if amount < 0:
        return jsonify({'error': '预算金额不能为负'}), 400

    b = Budget.set_budget(uid, month, category, amount)
    return jsonify(b.to_dict())


@budget_bp.route('', methods=['DELETE'])
@jwt_required()
def delete_budget():
    """删除某月某分类的预算"""
    uid = int(get_jwt_identity())
    data = request.get_json() or {}
    month = data.get('month', datetime.now().strftime('%Y-%m'))
    category = data.get('category', 'total')
    Budget.delete_budget(uid, month, category)
    return jsonify({'message': '已删除'})


@budget_bp.route('/usage', methods=['GET'])
@jwt_required()
def get_usage():
    """获取某月的预算使用情况（已花费 vs 预算）"""
    uid = int(get_jwt_identity())
    month = request.args.get('month', datetime.now().strftime('%Y-%m'))

    budgets = Budget.get_by_month(uid, month)
    if not budgets:
        return jsonify({'month': month, 'total': None, 'categories': []})

    # 查询该月所有支出
    year, mon = int(month[:4]), int(month[5:7])
    bills = Bill.query.filter_by(user_id=uid, type='支出').all()
    month_bills = [b for b in bills if b.bill_date.year == year and b.bill_date.month == mon]

    # 按子分类统计支出
    spent_by_cat = {}
    total_spent = 0.0
    for b in month_bills:
        key = b.sub_category or '未分类'
        spent_by_cat[key] = spent_by_cat.get(key, 0.0) + abs(b.money)
        total_spent += abs(b.money)

    result = {'month': month, 'total': None, 'categories': []}

    for bg in budgets:
        if bg.category == 'total':
            result['total'] = {
                'budget': bg.amount,
                'spent': round(total_spent, 2),
                'remaining': round(bg.amount - total_spent, 2),
                'percent': round(total_spent / bg.amount * 100, 1) if bg.amount > 0 else 0
            }
        else:
            spent = spent_by_cat.get(bg.category, 0.0)
            result['categories'].append({
                'category': bg.category,
                'budget': bg.amount,
                'spent': round(spent, 2),
                'remaining': round(bg.amount - spent, 2),
                'percent': round(spent / bg.amount * 100, 1) if bg.amount > 0 else 0
            })

    return jsonify(result)
