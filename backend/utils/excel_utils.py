import pandas as pd
from io import BytesIO
from models.bill import Bill
from extensions import db


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
