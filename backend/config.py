from datetime import timedelta


class Config:
    SECRET_KEY = 'bill_system_2025'

    # MySQL
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Xqy624070'
    MYSQL_DB = 'bill_system'

    # JWT
    JWT_SECRET_KEY = 'bill_sys_jwt_secret_2025'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
