from extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Integer, default=0)

    # ---------- 查询方法 ----------

    @staticmethod
    def login(username, password):
        return User.query.filter_by(username=username, password=password).first()

    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_all():
        return User.query.all()

    # ---------- 写入方法 ----------

    @staticmethod
    def add(username, password):
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update(user_id, username, password):
        user = User.query.get(user_id)
        if user:
            user.username = username
            user.password = password
            db.session.commit()

    @staticmethod
    def delete(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
