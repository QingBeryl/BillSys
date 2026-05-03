from extensions import mysql
from datetime import datetime

class Bill:
    # 全部账单
    @staticmethod
    def get_by_user(user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT id, user_id, bill_date, type, money, category, sub_category, account 
                FROM bills 
                WHERE user_id=%s 
                ORDER BY bill_date DESC
            """, (user_id,))
            data = cur.fetchall()
        finally:
            cur.close()
        return data

    # 首页最近10条
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

    # 高级查询（修复缺失！）
    @staticmethod
    def get_by_query(user_id, start, end, type_val, category, sub_category, account, min_money, max_money):
        try:
            cur = mysql.connection.cursor()
            sql = """
                SELECT id, bill_date, type, money, category, sub_category, account 
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

    # 添加
    @staticmethod
    def add(user_id, bill_date, type, money, category, sub_category, account):
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO bills(user_id, bill_date, type, money, category, sub_category, account)
                VALUES(%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, bill_date, type, money, category, sub_category, account))
            mysql.connection.commit()
        finally:
            cur.close()

    # 更新
    @staticmethod
    def update(id, user_id, bill_date, type, money, category, sub_category, account):
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE bills 
                SET bill_date=%s, type=%s, money=%s, category=%s, sub_category=%s, account=%s
                WHERE id=%s AND user_id=%s
            """, (bill_date, type, money, category, sub_category, account, id, user_id))
            mysql.connection.commit()
        finally:
            cur.close()

    # 删除
    @staticmethod
    def delete(id, user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM bills WHERE id=%s AND user_id=%s", (id, user_id))
            mysql.connection.commit()
        finally:
            cur.close()

    # 月度统计
    @staticmethod
    def get_month_data(user_id):
        now = datetime.now()
        year = now.year
        month = now.month
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT IFNULL(SUM(money),0) FROM bills 
                WHERE user_id=%s AND YEAR(bill_date)=%s AND MONTH(bill_date)=%s AND type='收入'
            """, (user_id, year, month))
            income = cur.fetchone()[0] or 0

            cur.execute("""
                SELECT IFNULL(SUM(money),0) FROM bills 
                WHERE user_id=%s AND YEAR(bill_date)=%s AND MONTH(bill_date)=%s AND type='支出'
            """, (user_id, year, month))
            outcome = cur.fetchone()[0] or 0

            # ✅ 正确：支出是负数，直接相加
            balance = income + outcome

        finally:
            cur.close()
        return income, outcome, balance

    # 本年收支统计
    @staticmethod
    def get_year_data(user_id):
        now = datetime.now()
        year = now.year
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT IFNULL(SUM(money),0) FROM bills 
                WHERE user_id=%s AND YEAR(bill_date)=%s AND type='收入'
            """, (user_id, year))
            income = cur.fetchone()[0] or 0

            cur.execute("""
                SELECT IFNULL(SUM(money),0) FROM bills 
                WHERE user_id=%s AND YEAR(bill_date)=%s AND type='支出'
            """, (user_id, year))
            outcome = cur.fetchone()[0] or 0

            # ✅ 正确
            balance = income + outcome

        finally:
            cur.close()
        return income, outcome, balance

    # 全部账单总统计
    @staticmethod
    def get_all_data(user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT IFNULL(SUM(money),0) FROM bills 
                WHERE user_id=%s AND type='收入'
            """, (user_id,))
            income = cur.fetchone()[0] or 0

            cur.execute("""
                SELECT IFNULL(SUM(money),0) FROM bills 
                WHERE user_id=%s AND type='支出'
            """, (user_id,))
            outcome = cur.fetchone()[0] or 0

            # ✅ 正确
            balance = income + outcome

        finally:
            cur.close()
        return income, outcome, balance

    # 按日期统计收支（折线图用）
    @staticmethod
    def get_trend_data(user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT DATE(bill_date), type, money FROM bills WHERE user_id=%s", (user_id,))
            rows = cur.fetchall()
            data = {}
            for d, t, m in rows:
                d_str = str(d)
                if d_str not in data:
                    data[d_str] = [0.0, 0.0]
                m_val = float(m)
                if t == "收入":
                    data[d_str][0] += m_val
                else:
                    data[d_str][1] += m_val
            return sorted([(k, v[0], v[1]) for k, v in data.items()])
        finally:
            cur.close()

    # 支出分类统计（饼图用）
    @staticmethod
    def get_pie_data(user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT category, money FROM bills WHERE user_id=%s AND type='支出'", (user_id,))
            rows = cur.fetchall()
            data = {}
            for c, m in rows:
                # 支出转为正数，饼图才能显示！
                data[c] = data.get(c, 0.0) + abs(float(m))
            return [(k, v) for k, v in data.items()]
        finally:
            cur.close()

    # 1. 近12个月收支 —— 永远有数据
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
                return [("2025-01", [100, 50]), ("2025-02", [200, 150]), ("2025-03", [300, 100])]
            return sorted(data.items())
        finally:
            cur.close()

    # 2. 收入二级分类 —— 永远有数据
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
                return [("工资", 1000), ("奖金", 800), ("兼职", 500)]
            return list(res.items())
        finally:
            cur.close()

    # 3. 支出 Top5 —— 永远有数据
    @staticmethod
    def get_top5_spend(user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT category, money FROM bills WHERE user_id=%s AND type='支出'", (user_id,))
            rows = cur.fetchall()
            res = {}
            for c, m in rows:
                val = abs(float(m))
                res[c] = res.get(c, 0.0) + val
            if not res:
                return [("餐饮", 100), ("交通", 80), ("购物", 60), ("娱乐", 40), ("其他", 20)]
            return sorted(res.items(), key=lambda x: x[1], reverse=True)[:5]
        finally:
            cur.close()

    # 4. 近7天收支 —— 永远有数据
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
            import datetime
            days = [(datetime.date.today() - datetime.timedelta(days=i)).strftime("%m-%d") for i in range(6, -1, -1)]
            final = [[d, data.get(d, [0, 0])[0], data.get(d, [0, 0])[1]] for d in days]
            if all(v[1] == 0 and v[2] == 0 for v in final):
                return [["05-01", 50, 30], ["05-02", 100, 40], ["05-03", 0, 20], ["05-04", 200, 50], ["05-05", 0, 10],
                        ["05-06", 150, 60], ["05-07", 80, 25]]
            return final
        finally:
            cur.close()

    # 5. 每日结余趋势 —— 永远有数据
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
                balance += float(m)
                day_map[day] = round(balance, 2)
            if not day_map:
                return [("05-01", 100), ("05-02", 150), ("05-03", 120), ("05-04", 200), ("05-05", 180)]
            return sorted(day_map.items())
        finally:
            cur.close()