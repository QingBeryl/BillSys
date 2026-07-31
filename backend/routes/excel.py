from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.excel_utils import export_excel, import_excel, generate_report

excel_bp = Blueprint('excel', __name__, url_prefix='/api/excel')


@excel_bp.route('/export', methods=['GET'])
@jwt_required()
def export():
    uid = int(get_jwt_identity())
    output = export_excel(uid)
    return send_file(
        output,
        download_name="bills.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True
    )


@excel_bp.route('/report', methods=['GET'])
@jwt_required()
def report():
    uid = int(get_jwt_identity())
    period_type = request.args.get('type', 'month')
    period_value = request.args.get('period', '')
    if not period_value:
        return jsonify({'error': '请指定时间段'}), 400
    output = generate_report(uid, period_type, period_value)
    filename = f"报表_{period_value}.xlsx"
    return send_file(
        output,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True
    )


@excel_bp.route('/import', methods=['POST'])
@jwt_required()
def import_file():
    uid = int(get_jwt_identity())
    file = request.files.get('file')
    if not file:
        return jsonify({'error': '请上传文件'}), 400

    if not file.filename.endswith(('.xlsx', '.xls')):
        return jsonify({'error': '仅支持 .xlsx 或 .xls 格式'}), 400

    count = import_excel(file, uid)
    return jsonify({'message': f'成功导入 {count} 条记录', 'count': count})
