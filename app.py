import os
os.environ['FLASK_ENV'] = 'production'

from flask import Flask, render_template, request, redirect, session, flash, send_file
from config import Config
from extensions import mysql
from models.user import User
from models.bill import Bill
from utils.excel_utils import export_excel, import_excel
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
mysql.init_app(app)

# 加速配置
app.config['TEMPLATES_AUTO_RELOAD'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# 分类
CATEGORIES = {
    '收入': ['理财盈利','兼职外快','助学金','利息','中奖','虚拟软件','其他','生活费'],
    '购物消费': ['生活用品','话费','手机数码','景区纪念','个护美妆','虚拟充值','学习用品','情趣用品','服饰运动','日常家居','装修装饰'],
    '食品餐饮': ['外卖','饮料酒水','晚餐','午餐','早餐','休闲零食','夜宵'],
    '校园生活': ['洗衣','电费','水费','文件打印','班费','团党费用','其他'],
    '文化教育': ['学费'],
    '出行交通': ['地铁','火车','打车'],
    '健康医疗': ['医院','校医务室','买药'],
    '送礼人情': ['红包']
}
ACCOUNTS = ['现金','校园一卡通','建设银行','支付宝','微信']

# ==================== 登录 ====================
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.login(username,password)
        if user:
            session['uid'] = user[0]
            session['username'] = user[1]
            session['is_admin'] = user[2]
            return redirect('/index')
        else:
            flash('用户名或密码错误')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ==================== 首页 ====================
@app.route('/index')
def index():
    if not session.get('uid'):
        return redirect('/')
    uid = session['uid']

    month_inc, month_out, month_bal = Bill.get_month_data(uid)
    year_inc, year_out, year_bal = Bill.get_year_data(uid)
    all_inc, all_out, all_bal = Bill.get_all_data(uid)
    bills = Bill.get_home_top10(uid)
    trend = Bill.get_trend_data(uid)
    pie = Bill.get_pie_data(uid)

    # 新增 5 个图表
    month12 = Bill.get_12month_data(uid)
    in_pie = Bill.get_income_pie(uid)
    top5 = Bill.get_top5_spend(uid)
    day7 = Bill.get_7day_data(uid)
    bal_trend = Bill.get_balance_trend(uid)

    return render_template('index.html',
        month_inc=month_inc, month_out=month_out, month_bal=month_bal,
        year_inc=year_inc, year_out=year_out, year_bal=year_bal,
        all_inc=all_inc, all_out=all_out, all_bal=all_bal,
        bills=bills, trend=trend, pie=pie,
        month12=month12, in_pie=in_pie, top5=top5, day7=day7, bal_trend=bal_trend
    )

# ==================== 收支记录 ====================
@app.route('/bill/list')
def bill_list():
    if not session.get('uid'): return redirect('/')
    bills = Bill.get_by_user(session['uid'])
    return render_template('bill_list.html', bills=bills, cats=CATEGORIES, accounts=ACCOUNTS)

@app.route('/bill/add')
def bill_add():
    if not session.get('uid'): return redirect('/')
    return render_template('add_bill.html', cats=CATEGORIES, accounts=ACCOUNTS)

@app.route('/bill/save', methods=['POST'])
def bill_save():
    uid = session.get('uid')
    data = request.form
    Bill.add(uid, data['date'], data['type'], data['money'], data['category'],
             data['sub_category'], data['account'], data['book'], data['refund'] or 0, data['remark'])
    return redirect('/bill/list')

@app.route('/bill/delete/<int:id>')
def bill_delete(id):
    Bill.delete(id, session.get('uid'))
    return redirect('/bill/list')

# ==================== 转账 ====================
@app.route('/transfer')
def transfer():
    return render_template('transfer.html', accounts=ACCOUNTS)

@app.route('/transfer/save', methods=['POST'])
def transfer_save():
    uid = session.get('uid')
    date = request.form['date']
    out_acc = request.form['out_account']
    in_acc = request.form['in_account']
    money = float(request.form['money'])
    remark = request.form['remark']
    Bill.add(uid, date, '支出', money, '转账', '转账', out_acc, '日常账本', 0, remark)
    Bill.add(uid, date, '收入', money, '转账', '转账', in_acc, '日常账本', 0, remark)
    return redirect('/bill/list')

# ==================== 查询 ====================
@app.route('/query')
def query():
    return render_template('query.html', cats=CATEGORIES, accounts=ACCOUNTS)


@app.route('/query/result', methods=['POST'])
def query_result():
    if not session.get('uid'):
        return redirect('/')

    data = request.form
    res = Bill.get_by_query(
        session.get('uid'),
        data.get('start'),
        data.get('end'),
        data.get('type'),
        data.get('category'),
        data.get('sub_category'),
        data.get('account'),
        data.get('min'),
        data.get('max')
    )

    return render_template('query.html', res=res, count=len(res), cats=CATEGORIES, accounts=ACCOUNTS)
# ==================== Excel ====================
# 导入导出页面
@app.route('/excel')
def excel_page():
    if not session.get('uid'):
        return redirect('/')
    return render_template('excel.html')

# 导入 Excel（只保留这一个！）
@app.route('/excel/import', methods=['POST'])
def excel_import():
    if not session.get('uid'):
        return redirect('/')
    file = request.files.get('file')
    if file:
        import_excel(file, session.get('uid'))
    return redirect('/excel')

# 导出 Excel
@app.route('/excel/export')
def excel_export():
    if not session.get('uid'):
        return redirect('/')
    output = export_excel(session.get('uid'))
    return send_file(
        output,
        download_name="账单.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ==================== 用户管理 ====================
@app.route('/user/manage')
def user_manage():
    if not session.get('is_admin'):
        return redirect('/index')
    users = User.get_all()
    return render_template('user_manager.html', users=users)

@app.route('/user/add', methods=['POST'])
def user_add():
    User.add(request.form['username'], request.form['password'])
    return redirect('/user/manage')

@app.route('/user/update', methods=['POST'])
def user_update():
    User.update(request.form['id'], request.form['username'], request.form['password'])
    return redirect('/user/manage')

@app.route('/user/delete/<int:id>')
def user_delete(id):
    User.delete(id)
    return redirect('/user/manage')

@app.route('/bill/edit/<int:id>')
def bill_edit(id):
    if not session.get('uid'): return redirect('/')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bills WHERE id=%s AND user_id=%s", (id, session.get('uid')))
    bill = cur.fetchone()
    cur.close()
    return render_template('edit_bill.html', bill=bill, cats=CATEGORIES, accounts=ACCOUNTS)

@app.route('/bill/edit_save/<int:id>', methods=['POST'])
def bill_edit_save(id):
    uid = session.get('uid')
    data = request.form
    Bill.update(id, uid, data['date'], data['type'], data['money'], data['category'],
             data['sub_category'], data['account'], data['book'], data['refund'] or 0, data['remark'])
    return redirect('/bill/list')

# ==================== 极速启动 ====================
if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        threaded=True,
        use_reloader=False
    )