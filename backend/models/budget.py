from extensions import db
from datetime import datetime


class Budget(db.Model):
    __tablename__ = 'budgets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    # 'total' 表示总预算，否则存分类名（如 '餐饮'）
    category = db.Column(db.String(50), nullable=False, default='total')
    amount = db.Column(db.Float, nullable=False, default=0)
    # 预算所属月份，格式 '2026-07'
    month = db.Column(db.String(7), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category': self.category,
            'amount': self.amount,
            'month': self.month
        }

    @staticmethod
    def get_by_month(user_id, month):
        return Budget.query.filter_by(user_id=user_id, month=month).all()

    @staticmethod
    def set_budget(user_id, month, category, amount):
        """创建或更新某月某分类的预算"""
        existing = Budget.query.filter_by(
            user_id=user_id, month=month, category=category
        ).first()
        if existing:
            existing.amount = amount
        else:
            existing = Budget(user_id=user_id, month=month,
                              category=category, amount=amount)
            db.session.add(existing)
        db.session.commit()
        return existing

    @staticmethod
    def delete_budget(user_id, month, category):
        Budget.query.filter_by(
            user_id=user_id, month=month, category=category
        ).delete()
        db.session.commit()
