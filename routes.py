from flask import Blueprint, render_template, request, redirect, session, flash, send_file
from models.user import User
from models.bill import Bill
from utils.excel_utils import export_excel, import_excel

# 主蓝图（所有功能统一注册到这里）
main_bp = Blueprint('main', __name__)

# 分类常量
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

# ==================== 登录/退出 ====================
@main_bp.route('/', methods=['GET','POST'])
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

@main_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ==================== 首页 ====================
@main_bp.route('/index')
def index():
    if not session.get('uid'):
        return redirect('/')
    income, outcome, balance = Bill.get_month_data(session['uid'])
    bills = Bill.get_by_user(session['uid'])[:10]
    return render_template('index.html', income=income, outcome=outcome, balance=balance, bills=bills)

# ==================== 收支记录 ====================
@main_bp.route('/bill/list')
def bill_list():
    if not session.get('uid'): return redirect('/')
    bills = Bill.get_by_user(session['uid'])
    return render_template('bill_list.html', bills=bills, cats=CATEGORIES, accounts=ACCOUNTS)

@main_bp.route('/bill/add')
def bill_add():
    if not session.get('uid'): return redirect('/')
    return render_template('add_bill.html', cats=CATEGORIES, accounts=ACCOUNTS)

@main_bp.route('/bill/save', methods=['POST'])
def bill_save():
    uid = session.get('uid')
    data = request.form
    Bill.add(uid, data['date'], data['type'], data['money'], data['category'],
             data['sub_category'], data['account'], data['book'], data['refund'] or 0, data['remark'])
    return redirect('/bill/list')

@main_bp.route('/bill/delete/<int:id>')
def bill_delete(id):
    Bill.delete(id, session.get('uid'))
    return redirect('/bill/list')

# ==================== 转账 ====================
@main_bp.route('/transfer')
def transfer():
    return render_template('transfer.html', accounts=ACCOUNTS)

@main_bp.route('/transfer/save', methods=['POST'])
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

# ==================== 查询记录 ====================
@main_bp.route('/query')
def query():
    return render_template('query.html', cats=CATEGORIES, accounts=ACCOUNTS)

@main_bp.route('/query/result', methods=['POST'])
def query_result():
    data = request.form
    res = Bill.get_by_query(session.get('uid'), data['start'], data['end'], data['type'],
                            data['min'], data['max'], data['category'], data['sub_category'],
                            data['account'], data['book'])
    return render_template('query.html', cats=CATEGORIES, accounts=ACCOUNTS, res=res, count=len(res))

# ==================== Excel导入导出 ====================
@main_bp.route('/excel')
def excel():
    return render_template('excel.html')

@main_bp.route('/excel/export')
def excel_export():
    f = export_excel(session.get('uid'))
    return send_file(f, as_attachment=True)

@main_bp.route('/excel/import', methods=['POST'])
def excel_import():
    file = request.files['file']
    import_excel(file, session.get('uid'))
    return redirect('/excel')

# ==================== 用户管理 ====================
@main_bp.route('/user/manage')
def user_manage():
    if not session.get('is_admin'):
        return redirect('/index')
    users = User.get_all()
    return render_template('user_manager.html', users=users)

@main_bp.route('/user/add', methods=['POST'])
def user_add():
    User.add(request.form['username'], request.form['password'])
    return redirect('/user/manage')

@main_bp.route('/user/update', methods=['POST'])
def user_update():
    User.update(request.form['id'], request.form['username'], request.form['password'])
    return redirect('/user/manage')

@main_bp.route('/user/delete/<int:id>')
def user_delete(id):
    User.delete(id)
    return redirect('/user/manage')