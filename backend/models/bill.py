from extensions import mysql
from datetime import datetime, date, timedelta


class Bill:
    @staticmethod
    def get_by_user(user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT id, user_id, bill_date, type, money, category, sub_category,
                       account, book_name, refund, remark
                FROM bills
                WHERE user_id=%s
                ORDER BY bill_date DESC
            """, (user_id,))
            data = cur.fetchall()
        finally:
            cur.close()
        return data

    @staticmethod
    def get_by_id(bill_id, user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT id, user_id, bill_date, type, money, category, sub_category,
                       account, book_name, refund, remark
                FROM bills
                WHERE id=%s AND user_id=%s
            """, (bill_id, user_id))
            data = cur.fetchone()
        finally:
            cur.close()
        return data

    @staticmethod
    def get_home_top10(user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT bill_date, type, money, category, sub_category
                FROM bills
                WHERE user_id=%s
                ORDER BY bill_date DESC
                LIMIT 10
            """, (user_id,))
            data = cur.fetchall()
        finally:
            cur.close()
        return data

    @staticmethod
    def get_by_query(user_id, start, end, type_val, category, sub_category, account, min_money, max_money):
        try:
            cur = mysql.connection.cursor()
            sql = """
                SELECT id, bill_date, type, money, category, sub_category, account, book_name, refund, remark
                FROM bills
                WHERE user_id=%s
            """
            params = [user_id]

            if start:
                sql += " AND bill_date >= %s"
                params.append(start)
            if end:
                sql += " AND bill_date <= %s"
                params.append(end)
            if type_val:
                sql += " AND type = %s"
                params.append(type_val)
            if category:
                sql += " AND category = %s"
                params.append(category)
            if sub_category:
                sql += " AND sub_category = %s"
                params.append(sub_category)
            if account:
                sql += " AND account = %s"
                params.append(account)
            if min_money:
                sql += " AND money >= %s"
                params.append(min_money)
            if max_money:
                sql += " AND money <= %s"
                params.append(max_money)

            sql += " ORDER BY bill_date DESC"
            cur.execute(sql, params)
            return cur.fetchall()
        finally:
            cur.close()

    @staticmethod
    def add(user_id, bill_date, type_val, money, category, sub_category, account,
            book_name='日常账本', refund=0, remark=''):
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO bills(user_id, bill_date, type, money, category, sub_category, account, book_name, refund, remark)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, bill_date, type_val, money, category, sub_category, account, book_name, refund, remark))
            mysql.connection.commit()
        finally:
            cur.close()

    @staticmethod
    def update(bill_id, user_id, bill_date, type_val, money, category, sub_category, account,
               book_name='日常账本', refund=0, remark=''):
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE bills
                SET bill_date=%s, type=%s, money=%s, category=%s, sub_category=%s,
                    account=%s, book_name=%s, refund=%s, remark=%s
                WHERE id=%s AND user_id=%s
            """, (bill_date, type_val, money, category, sub_category, account,
                  book_name, refund, remark, bill_id, user_id))
            mysql.connection.commit()
        finally:
            cur.close()

    @staticmethod
    def delete(bill_id, user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM bills WHERE id=%s AND user_id=%s", (bill_id, user_id))
            mysql.connection.commit()
        finally:
            cur.close()

    # ==================== 统计 ====================

    @staticmethod
    def get_month_data(user_id):
        now = datetime.now()
        year, month = now.year, now.month
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT IFNULL(SUM(money),0) FROM bills
                WHERE user_id=%s AND YEAR(bill_date)=%s AND MONTH(bill_date)=%s AND type='收入'
            """, (user_id, year, month))
            income = float(cur.fetchone()[0] or 0)

            cur.execute("""
                SELECT IFNULL(SUM(money),0) FROM bills
                WHERE user_id=%s AND YEAR(bill_date)=%s AND MONTH(bill_date)=%s AND type='支出'
            """, (user_id, year, month))
            expense = float(cur.fetchone()[0] or 0)
        finally:
            cur.close()
        return income, expense, income - expense

    @staticmethod
    def get_year_data(user_id):
        year = datetime.now().year
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT IFNULL(SUM(money),0) FROM bills
                WHERE user_id=%s AND YEAR(bill_date)=%s AND type='收入'
            """, (user_id, year))
            income = float(cur.fetchone()[0] or 0)

            cur.execute("""
                SELECT IFNULL(SUM(money),0) FROM bills
                WHERE user_id=%s AND YEAR(bill_date)=%s AND type='支出'
            """, (user_id, year))
            expense = float(cur.fetchone()[0] or 0)
        finally:
            cur.close()
        return income, expense, income - expense

    @staticmethod
    def get_all_data(user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT IFNULL(SUM(money),0) FROM bills WHERE user_id=%s AND type='收入'", (user_id,))
            income = float(cur.fetchone()[0] or 0)

            cur.execute("SELECT IFNULL(SUM(money),0) FROM bills WHERE user_id=%s AND type='支出'", (user_id,))
            expense = float(cur.fetchone()[0] or 0)
        finally:
            cur.close()
        return income, expense, income - expense

    @staticmethod
    def get_12month_data(user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT bill_date, type, money FROM bills WHERE user_id=%s", (user_id,))
            rows = cur.fetchall()
            data = {}
            for d, t, m in rows:
                month = d.strftime("%Y-%m")
                if month not in data:
                    data[month] = [0.0, 0.0]
                if t == "收入":
                    data[month][0] += float(m)
                else:
                    data[month][1] += abs(float(m))
            if not data:
                return [{"month": "2025-01", "income": 100, "expense": 50},
                        {"month": "2025-02", "income": 200, "expense": 150},
                        {"month": "2025-03", "income": 300, "expense": 100}]
            return [{"month": k, "income": round(v[0], 2), "expense": round(v[1], 2)}
                    for k, v in sorted(data.items())]
        finally:
            cur.close()

    @staticmethod
    def get_pie_data(user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT category, money FROM bills WHERE user_id=%s AND type='支出'", (user_id,))
            rows = cur.fetchall()
            data = {}
            for c, m in rows:
                data[c] = data.get(c, 0.0) + abs(float(m))
            if not data:
                return [{"name": "餐饮", "value": 100}, {"name": "交通", "value": 80},
                        {"name": "购物", "value": 60}]
            return [{"name": k, "value": round(v, 2)} for k, v in data.items()]
        finally:
            cur.close()

    @staticmethod
    def get_income_pie(user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT sub_category, money FROM bills WHERE user_id=%s AND type='收入'", (user_id,))
            rows = cur.fetchall()
            res = {}
            for c, m in rows:
                if c:
                    res[c] = res.get(c, 0.0) + float(m)
            if not res:
                return [{"name": "工资", "value": 1000}, {"name": "奖金", "value": 800},
                        {"name": "兼职", "value": 500}]
            return [{"name": k, "value": round(v, 2)} for k, v in res.items()]
        finally:
            cur.close()

    @staticmethod
    def get_top5_spend(user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT category, money FROM bills WHERE user_id=%s AND type='支出'", (user_id,))
            rows = cur.fetchall()
            res = {}
            for c, m in rows:
                res[c] = res.get(c, 0.0) + abs(float(m))
            if not res:
                return [{"name": "餐饮", "value": 100}, {"name": "交通", "value": 80},
                        {"name": "购物", "value": 60}, {"name": "娱乐", "value": 40},
                        {"name": "其他", "value": 20}]
            sorted_items = sorted(res.items(), key=lambda x: x[1], reverse=True)[:5]
            return [{"name": k, "value": round(v, 2)} for k, v in sorted_items]
        finally:
            cur.close()

    @staticmethod
    def get_7day_data(user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT bill_date, type, money FROM bills WHERE user_id=%s", (user_id,))
            rows = cur.fetchall()
            data = {}
            for d, t, m in rows:
                day = d.strftime("%m-%d")
                if day not in data:
                    data[day] = [0.0, 0.0]
                if t == "收入":
                    data[day][0] += float(m)
                else:
                    data[day][1] += abs(float(m))
            days = [(date.today() - timedelta(days=i)).strftime("%m-%d") for i in range(6, -1, -1)]
            final = [{"day": d, "income": round(data.get(d, [0, 0])[0], 2),
                      "expense": round(data.get(d, [0, 0])[1], 2)} for d in days]
            if all(v["income"] == 0 and v["expense"] == 0 for v in final):
                return [{"day": "05-01", "income": 50, "expense": 30},
                        {"day": "05-02", "income": 100, "expense": 40},
                        {"day": "05-03", "income": 0, "expense": 20},
                        {"day": "05-04", "income": 200, "expense": 50},
                        {"day": "05-05", "income": 0, "expense": 10},
                        {"day": "05-06", "income": 150, "expense": 60},
                        {"day": "05-07", "income": 80, "expense": 25}]
            return final
        finally:
            cur.close()

    @staticmethod
    def get_balance_trend(user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT bill_date, type, money FROM bills WHERE user_id=%s ORDER BY bill_date", (user_id,))
            rows = cur.fetchall()
            balance = 0.0
            day_map = {}
            for d, t, m in rows:
                day = d.strftime("%m-%d")
                if t == "收入":
                    balance += float(m)
                else:
                    balance -= abs(float(m))
                day_map[day] = round(balance, 2)
            if not day_map:
                return [{"day": "05-01", "balance": 100}, {"day": "05-02", "balance": 150},
                        {"day": "05-03", "balance": 120}, {"day": "05-04", "balance": 200},
                        {"day": "05-05", "balance": 180}]
            return [{"day": k, "balance": v} for k, v in sorted(day_map.items())]
        finally:
            cur.close()
