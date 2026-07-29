import pandas as pd
from extensions import mysql
from io import BytesIO


def export_excel(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT bill_date, type, money, category, sub_category, account
        FROM bills
        WHERE user_id = %s
        ORDER BY bill_date DESC
    """, (user_id,))
    data = cur.fetchall()
    cur.close()

    columns = ['日期', '收支类型', '金额', '类别', '二级分类', '账户']
    rows = []
    for row in data:
        rows.append([
            row[0].strftime('%Y-%m-%d') if hasattr(row[0], 'strftime') else str(row[0]),
            row[1], float(row[2]), row[3], row[4], row[5]
        ])

    df = pd.DataFrame(rows, columns=columns)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output


def import_excel(file, user_id):
    df = pd.read_excel(file)
    cur = mysql.connection.cursor()
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
            cur.execute("""
                INSERT INTO bills(user_id, bill_date, type, money, category, sub_category, account)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, bill_date, type_val, money, category, sub_category, account))
            count += 1

    mysql.connection.commit()
    cur.close()
    return count
