from flask import Blueprint, jsonify

meta_bp = Blueprint('meta', __name__, url_prefix='/api')

CATEGORIES = {
    '收入': ['意外之财', '薪资酬劳', '兼职副业', '投资理财', '礼金红包', '退款报销', '其他'],
    '支出': ['水电燃气', '出行交通', '健康医疗', '食品餐饮', '社交人情', '柴米油盐',
             '话费', '购物消费', '教育学习', '居住房租', '休闲娱乐', '其他']
}

ACCOUNTS = ['现金', '校园一卡通', '建设银行', '支付宝', '微信']


@meta_bp.route('/meta', methods=['GET'])
def get_meta():
    return jsonify({'categories': CATEGORIES, 'accounts': ACCOUNTS})
