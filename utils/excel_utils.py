import pandas as pd
from extensions import mysql
from io import BytesIO


def export_excel(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT bill_date, type, money, category, sub_category, account
                FROM bills
                WHERE user_id = %s
                """, (user_id,))
    data = cur.fetchall()
    columns = ['日期', '收支类型', '金额', '类别', '二级分类', '账户']
    df = pd.DataFrame(data, columns=columns)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    cur.close()
    return output


def import_excel(file, user_id):
    df = pd.read_excel(file)
    cur = mysql.connection.cursor()

    for _, row in df.iterrows():
        # 核心修复：把 NaN 空值 替换成 空字符串 ''
        row = row.where(pd.notnull(row), None)

        sql = """
              INSERT INTO bills(user_id, bill_date, type, money, category, sub_category, account)
              VALUES (%s, %s, %s, %s, %s, %s, %s) \
              """
        # 安全读取，空值不报错
        bill_date = row.get('日期')
        type_val = row.get('收支类型')
        money = row.get('金额')
        category = row.get('类别')
        sub_category = row.get('二级分类')
        account = row.get('账户')

        cur.execute(sql, (
            user_id, bill_date, type_val, money, category, sub_category, account
        ))

    mysql.connection.commit()
    cur.close()