from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from extensions import mysql, jwt

from routes.auth import auth_bp
from routes.meta import meta_bp
from routes.bills import bills_bp
from routes.stats import stats_bp
from routes.transfer import transfer_bp
from routes.excel import excel_bp
from routes.users import users_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    mysql.init_app(app)
    jwt.init_app(app)

    # CORS：允许前端dev server跨域
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(meta_bp)
    app.register_blueprint(bills_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(transfer_bp)
    app.register_blueprint(excel_bp)
    app.register_blueprint(users_bp)

    # 全局错误处理
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': '接口不存在'}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'error': '服务器内部错误'}), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True)
