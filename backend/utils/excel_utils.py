import pandas as pd
from io import BytesIO
from models.bill import Bill
from extensions import db
from datetime import datetime


def export_excel(user_id):
    bills = Bill.query.filter_by(user_id=user_id).order_by(Bill.bill_date.desc()).all()

    columns = ['日期', '收支类型', '金额', '类别', '二级分类', '账户']
    rows = []
    for b in bills:
        rows.append([
            b.bill_date.strftime('%Y-%m-%d') if b.bill_date else '',
            b.type, b.money, b.category, b.sub_category, b.account
        ])

    df = pd.DataFrame(rows, columns=columns)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output


def generate_report(user_id, period_type, period_value):
    """
    生成月度/年度报表
    period_type: 'month' 或 'year'
    period_value: '2026-07' 或 '2026'
    """
    bills = Bill.query.filter_by(user_id=user_id).all()

    # 筛选当期账单
    current_bills = []
    prev_bills = []

    if period_type == 'month':
        year, month = int(period_value[:4]), int(period_value[5:7])
        # 上一期
        if month == 1:
            prev_year, prev_month = year - 1, 12
        else:
            prev_year, prev_month = year, month - 1

        for b in bills:
            if b.bill_date.year == year and b.bill_date.month == month:
                current_bills.append(b)
            elif b.bill_date.year == prev_year and b.bill_date.month == prev_month:
                prev_bills.append(b)
        period_label = period_value
        prev_label = f"{prev_year:04d}-{prev_month:02d}"
    else:
        year = int(period_value)
        for b in bills:
            if b.bill_date.year == year:
                current_bills.append(b)
            elif b.bill_date.year == year - 1:
                prev_bills.append(b)
        period_label = f"{period_value}年"
        prev_label = f"{year - 1}年"

    # === Sheet1: 总览 ===
    cur_income = sum(b.money for b in current_bills if b.type == '收入')
    cur_expense = sum(abs(b.money) for b in current_bills if b.type == '支出')
    prev_income = sum(b.money for b in prev_bills if b.type == '收入')
    prev_expense = sum(abs(b.money) for b in prev_bills if b.type == '支出')

    summary_data = {
        '项目': ['收入', '支出', '结余'],
        period_label: [round(cur_income, 2), round(cur_expense, 2), round(cur_income - cur_expense, 2)],
        prev_label: [round(prev_income, 2), round(prev_expense, 2), round(prev_income - prev_expense, 2)],
    }
    # 环比变化
    income_change = round(cur_income - prev_income, 2)
    expense_change = round(cur_expense - prev_expense, 2)
    balance_change = round((cur_income - cur_expense) - (prev_income - prev_expense), 2)
    summary_data['环比变化'] = [income_change, expense_change, balance_change]

    df_summary = pd.DataFrame(summary_data)

    # === Sheet2: 支出分类明细 ===
    expense_by_cat = {}
    for b in current_bills:
        if b.type == '支出':
            key = b.category or '未分类'
            expense_by_cat[key] = expense_by_cat.get(key, 0.0) + abs(b.money)

    if expense_by_cat:
        sorted_cats = sorted(expense_by_cat.items(), key=lambda x: x[1], reverse=True)
        df_expense = pd.DataFrame([
            {'分类': k, '金额': round(v, 2), '占比': f"{v / cur_expense * 100:.1f}%" if cur_expense > 0 else "0%"}
            for k, v in sorted_cats
        ])
    else:
        df_expense = pd.DataFrame(columns=['分类', '金额', '占比'])

    # === Sheet3: 收入分类明细 ===
    income_by_cat = {}
    for b in current_bills:
        if b.type == '收入':
            key = b.sub_category or b.category or '未分类'
            income_by_cat[key] = income_by_cat.get(key, 0.0) + b.money

    if income_by_cat:
        sorted_inc = sorted(income_by_cat.items(), key=lambda x: x[1], reverse=True)
        df_income = pd.DataFrame([
            {'分类': k, '金额': round(v, 2), '占比': f"{v / cur_income * 100:.1f}%" if cur_income > 0 else "0%"}
            for k, v in sorted_inc
        ])
    else:
        df_income = pd.DataFrame(columns=['分类', '金额', '占比'])

    # === Sheet4: 当期所有账单 ===
    columns = ['日期', '收支类型', '金额', '类别', '二级分类', '账户', '备注']
    rows = []
    for b in sorted(current_bills, key=lambda x: x.bill_date, reverse=True):
        rows.append([
            b.bill_date.strftime('%Y-%m-%d') if b.bill_date else '',
            b.type, b.money, b.category, b.sub_category, b.account, b.remark or ''
        ])
    df_bills = pd.DataFrame(rows, columns=columns)

    # 写入Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_summary.to_excel(writer, sheet_name='总览', index=False)
        df_expense.to_excel(writer, sheet_name='支出分类', index=False)
        df_income.to_excel(writer, sheet_name='收入分类', index=False)
        df_bills.to_excel(writer, sheet_name='账单明细', index=False)
    output.seek(0)
    return output


def import_excel(file, user_id):
    df = pd.read_excel(file)
    count = 0

    for _, row in df.iterrows():
        row = row.where(pd.notnull(row), None)
        bill_date = row.get('日期')
        type_val = row.get('收支类型')
        money = row.get('金额')
        category = row.get('类别')
        sub_category = row.get('二级分类')
        account = row.get('账户')

        if bill_date and type_val and money:
            Bill.add(user_id, str(bill_date), type_val, money,
                     category or '', sub_category or '', account or '')
            count += 1

    return count
