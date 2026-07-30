from extensions import db
from datetime import datetime, date, timedelta
from sqlalchemy import func, extract


class Bill(db.Model):
    __tablename__ = 'bills'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    bill_date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(10), nullable=False)       # 收入 / 支出
    money = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), default='')
    sub_category = db.Column(db.String(50), default='')
    account = db.Column(db.String(50), default='')
    book_name = db.Column(db.String(50), default='日常账本')
    refund = db.Column(db.Float, default=0)
    remark = db.Column(db.String(255), default='')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'bill_date': self.bill_date.strftime('%Y-%m-%d %H:%M:%S') if self.bill_date else '',
            'type': self.type,
            'money': self.money,
            'category': self.category,
            'sub_category': self.sub_category,
            'account': self.account,
            'book_name': self.book_name,
            'refund': self.refund or 0,
            'remark': self.remark or ''
        }

    # ---------- CRUD ----------

    @staticmethod
    def get_by_user(user_id):
        return Bill.query.filter_by(user_id=user_id).order_by(Bill.bill_date.desc()).all()

    @staticmethod
    def get_by_id(bill_id, user_id):
        return Bill.query.filter_by(id=bill_id, user_id=user_id).first()

    @staticmethod
    def get_home_top10(user_id):
        return Bill.query.filter_by(user_id=user_id).order_by(Bill.bill_date.desc()).limit(10).all()

    @staticmethod
    def get_by_query(user_id, start, end, type_val, category, sub_category, account, min_money, max_money):
        q = Bill.query.filter_by(user_id=user_id)
        if start:
            q = q.filter(Bill.bill_date >= start)
        if end:
            q = q.filter(Bill.bill_date <= end)
        if type_val:
            q = q.filter(Bill.type == type_val)
        if category:
            q = q.filter(Bill.category == category)
        if sub_category:
            q = q.filter(Bill.sub_category == sub_category)
        if account:
            q = q.filter(Bill.account == account)
        if min_money:
            q = q.filter(Bill.money >= float(min_money))
        if max_money:
            q = q.filter(Bill.money <= float(max_money))
        return q.order_by(Bill.bill_date.desc()).all()

    @staticmethod
    def add(user_id, bill_date, type_val, money, category, sub_category, account,
            book_name='日常账本', refund=0, remark=''):
        # bill_date 可能是字符串，转为 datetime
        if isinstance(bill_date, str):
            for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
                try:
                    bill_date = datetime.strptime(bill_date, fmt)
                    break
                except ValueError:
                    continue
        bill = Bill(
            user_id=user_id, bill_date=bill_date, type=type_val,
            money=float(money), category=category, sub_category=sub_category,
            account=account, book_name=book_name, refund=float(refund or 0),
            remark=remark or ''
        )
        db.session.add(bill)
        db.session.commit()
        return bill

    @staticmethod
    def update(bill_id, user_id, bill_date, type_val, money, category, sub_category, account,
               book_name='日常账本', refund=0, remark=''):
        bill = Bill.query.filter_by(id=bill_id, user_id=user_id).first()
        if not bill:
            return
        if isinstance(bill_date, str):
            for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
                try:
                    bill_date = datetime.strptime(bill_date, fmt)
                    break
                except ValueError:
                    continue
        bill.bill_date = bill_date
        bill.type = type_val
        bill.money = float(money)
        bill.category = category
        bill.sub_category = sub_category
        bill.account = account
        bill.book_name = book_name
        bill.refund = float(refund or 0)
        bill.remark = remark or ''
        db.session.commit()

    @staticmethod
    def delete(bill_id, user_id):
        bill = Bill.query.filter_by(id=bill_id, user_id=user_id).first()
        if bill:
            db.session.delete(bill)
            db.session.commit()

    # ---------- 统计 ----------

    @staticmethod
    def _sum_by(user_id, type_val, year=None, month=None):
        q = db.session.query(func.coalesce(func.sum(Bill.money), 0)).filter(
            Bill.user_id == user_id, Bill.type == type_val
        )
        if year:
            q = q.filter(extract('year', Bill.bill_date) == year)
        if month:
            q = q.filter(extract('month', Bill.bill_date) == month)
        return float(q.scalar() or 0)

    @staticmethod
    def get_month_data(user_id):
        now = datetime.now()
        income = Bill._sum_by(user_id, '收入', now.year, now.month)
        expense = Bill._sum_by(user_id, '支出', now.year, now.month)
        return income, expense, income - expense

    @staticmethod
    def get_year_data(user_id):
        year = datetime.now().year
        income = Bill._sum_by(user_id, '收入', year)
        expense = Bill._sum_by(user_id, '支出', year)
        return income, expense, income - expense

    @staticmethod
    def get_all_data(user_id):
        income = Bill._sum_by(user_id, '收入')
        expense = Bill._sum_by(user_id, '支出')
        return income, expense, income - expense

    @staticmethod
    def get_12month_data(user_id):
        bills = Bill.query.filter_by(user_id=user_id).all()
        data = {}
        for b in bills:
            month = b.bill_date.strftime("%Y-%m")
            if month not in data:
                data[month] = [0.0, 0.0]
            if b.type == "收入":
                data[month][0] += b.money
            else:
                data[month][1] += abs(b.money)
        if not data:
            return [{"month": "2025-01", "income": 100, "expense": 50},
                    {"month": "2025-02", "income": 200, "expense": 150},
                    {"month": "2025-03", "income": 300, "expense": 100}]
        return [{"month": k, "income": round(v[0], 2), "expense": round(v[1], 2)}
                for k, v in sorted(data.items())]

    @staticmethod
    def get_pie_data(user_id):
        bills = Bill.query.filter_by(user_id=user_id, type='支出').all()
        data = {}
        for b in bills:
            data[b.category] = data.get(b.category, 0.0) + abs(b.money)
        if not data:
            return [{"name": "餐饮", "value": 100}, {"name": "交通", "value": 80},
                    {"name": "购物", "value": 60}]
        return [{"name": k, "value": round(v, 2)} for k, v in data.items()]

    @staticmethod
    def get_income_pie(user_id):
        bills = Bill.query.filter_by(user_id=user_id, type='收入').all()
        res = {}
        for b in bills:
            if b.sub_category:
                res[b.sub_category] = res.get(b.sub_category, 0.0) + b.money
        if not res:
            return [{"name": "工资", "value": 1000}, {"name": "奖金", "value": 800},
                    {"name": "兼职", "value": 500}]
        return [{"name": k, "value": round(v, 2)} for k, v in res.items()]

    @staticmethod
    def get_top5_spend(user_id):
        bills = Bill.query.filter_by(user_id=user_id, type='支出').all()
        res = {}
        for b in bills:
            res[b.category] = res.get(b.category, 0.0) + abs(b.money)
        if not res:
            return [{"name": "餐饮", "value": 100}, {"name": "交通", "value": 80},
                    {"name": "购物", "value": 60}, {"name": "娱乐", "value": 40},
                    {"name": "其他", "value": 20}]
        sorted_items = sorted(res.items(), key=lambda x: x[1], reverse=True)[:5]
        return [{"name": k, "value": round(v, 2)} for k, v in sorted_items]

    @staticmethod
    def get_7day_data(user_id):
        bills = Bill.query.filter_by(user_id=user_id).all()
        data = {}
        for b in bills:
            day = b.bill_date.strftime("%m-%d")
            if day not in data:
                data[day] = [0.0, 0.0]
            if b.type == "收入":
                data[day][0] += b.money
            else:
                data[day][1] += abs(b.money)
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

    @staticmethod
    def get_balance_trend(user_id):
        bills = Bill.query.filter_by(user_id=user_id).order_by(Bill.bill_date).all()
        balance = 0.0
        day_map = {}
        for b in bills:
            day = b.bill_date.strftime("%m-%d")
            if b.type == "收入":
                balance += b.money
            else:
                balance -= abs(b.money)
            day_map[day] = round(balance, 2)
        if not day_map:
            return [{"day": "05-01", "balance": 100}, {"day": "05-02", "balance": 150},
                    {"day": "05-03", "balance": 120}, {"day": "05-04", "balance": 200},
                    {"day": "05-05", "balance": 180}]
        return [{"day": k, "balance": v} for k, v in sorted(day_map.items())]
