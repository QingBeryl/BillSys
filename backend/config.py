import os
from datetime import timedelta


class Config:
    SECRET_KEY = 'bill_system_2025'

    # 数据库 —— 默认用 SQLite（无需安装，文件即数据库）
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'billsys.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 上线时注释掉上面两行，取消下面这段即可切换到 MySQL
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:你的密码@localhost/bill_system'

    # JWT
    JWT_SECRET_KEY = 'bill_sys_jwt_secret_2025'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
