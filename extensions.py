from flask_mysqldb import MySQL

mysql = MySQL()

# 数据库连接池配置（解决慢核心）
def init_mysql(app):
    app.config['MYSQL_MAX_CONNECTIONS'] = 20  # 连接池
    app.config['MYSQL_CONNECTION_TIMEOUT'] = 10
    app.config['MYSQL_READ_DEFAULT_GROUP'] = 'option'
    mysql.init_app(app)