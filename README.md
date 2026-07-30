# BillSys - 个人账单管理系统

前后端分离的个人财务管理平台，支持账单增删改查、多维度统计查询、ECharts 可视化图表、Excel 导入导出、账户转账、JWT 鉴权与管理员权限控制。

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | Python Flask 3.x（Blueprint 模块化） |
| ORM | Flask-SQLAlchemy（SQLite 开发 / MySQL 生产） |
| 鉴权 | Flask-JWT-Extended（24h Token） |
| 数据处理 | Pandas + openpyxl（Excel 导入导出） |
| 前端框架 | Vue 3（Composition API）+ Vite 5 |
| UI 组件库 | Element Plus + @element-plus/icons-vue |
| 图表 | ECharts 5 |
| 状态管理 | Pinia |
| HTTP 请求 | Axios（拦截器统一携带 Token） |

## 项目结构

```
02-BillSys-master/
├── backend/                  # Flask 后端（纯 REST API，port 5000）
│   ├── app.py                # 应用入口，create_app 工厂模式
│   ├── config.py             # 配置（数据库 URI、JWT 密钥与过期时间）
│   ├── extensions.py         # 扩展实例（db, jwt）
│   ├── models/               # 数据模型（SQLAlchemy ORM）
│   │   ├── user.py           # 用户模型（CRUD + 登录验证）
│   │   └── bill.py           # 账单模型（CRUD + 多条件查询 + 统计聚合）
│   ├── routes/               # 路由蓝图（7 个 Blueprint）
│   │   ├── auth.py           # 登录 / 注册 / 当前用户
│   │   ├── bills.py          # 账单 CRUD + 高级组合查询
│   │   ├── stats.py          # 统计（月/年/累计/12月趋势/饼图/Top5/7日/结余）
│   │   ├── transfer.py       # 账户间转账
│   │   ├── excel.py          # Excel 导入 / 导出
│   │   ├── users.py          # 用户管理（admin_required 装饰器）
│   │   └── meta.py           # 元数据（分类体系 + 账户列表）
│   ├── utils/
│   │   └── excel_utils.py    # Pandas 读写 Excel 逻辑
│   └── requirements.txt
├── frontend/                 # Vue 3 前端（SPA，port 3000）
│   ├── src/
│   │   ├── api/              # Axios 封装（auth / bills / stats / transfer / excel / users）
│   │   ├── router/           # Vue Router + 登录导航守卫
│   │   ├── stores/           # Pinia（用户状态）
│   │   └── views/            # 页面组件
│   │       ├── Login.vue / Register.vue
│   │       ├── Layout.vue    # 侧边栏布局壳
│   │       ├── Dashboard.vue # 仪表盘（统计卡片 + 图表）
│   │       ├── BillList.vue / BillForm.vue
│   │       ├── Query.vue     # 高级查询
│   │       ├── Transfer.vue  # 转账
│   │       ├── Excel.vue     # 导入导出
│   │       └── UserManage.vue# 用户管理（管理员）
│   ├── package.json
│   └── vite.config.js        # dev server port 3000 + /api 代理到 5000
└── README.md
```

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+

### 后端

```bash
cd backend
pip install -r requirements.txt
python app.py
```

启动后监听 `http://127.0.0.1:5000`，首次运行自动创建 `billsys.db`（SQLite 零配置）。

### 前端

```bash
cd frontend
npm install
npm run dev
```

启动后访问 `http://localhost:3000`，Vite 自动将 `/api` 请求代理到后端 5000 端口。

### 生产构建

```bash
cd frontend
npm run build    # 产物输出到 frontend/dist/
```

## 功能一览

- 用户注册 / 登录（JWT 鉴权，Token 24h 过期，前端路由守卫）
- 账单增删改查 + 多条件组合查询（日期范围、类型、分类、账户、金额区间）
- 仪表盘：月度 / 年度 / 累计收支统计卡片
- 图表：12 月收支趋势折线图、支出分类饼图、收入来源饼图、支出 Top5、近 7 日趋势、资产结余曲线
- 账户转账（自动生成一收一支出两条记录，分类标记为"转账"）
- Excel 导入（.xlsx / .xls）/ 导出
- 用户管理（管理员专属：查看、新增、编辑、删除用户）
- 分类元数据接口（前端下拉选项由后端统一维护）

## 数据模型

### User

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | 自增主键 |
| username | String(50) | 唯一，2-20 字符 |
| password | String(255) | 明文存储（学习项目） |
| is_admin | Integer | 0 普通用户 / 1 管理员 |

### Bill

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | 自增主键 |
| user_id | Integer | 所属用户 |
| bill_date | DateTime | 账单日期 |
| type | String(10) | "收入" / "支出" |
| money | Float | 金额 |
| category | String(50) | 一级分类 |
| sub_category | String(50) | 二级分类 |
| account | String(50) | 账户（现金/支付宝/微信等） |
| book_name | String(50) | 账本名，默认"日常账本" |
| refund | Float | 退款金额，默认 0 |
| remark | String(255) | 备注 |

## 分类与账户体系

后端 `/api/meta` 接口统一提供分类和账户选项，前端下拉框由此驱动：

**支出分类：** 购物消费、食品餐饮、校园生活、文化教育、出行交通、健康医疗、送礼人情（各含二级子分类）

**收入分类：** 理财盈利、兼职外快、助学金、利息、中奖、虚拟软件、生活费、其他

**账户：** 现金、校园一卡通、建设银行、支付宝、微信

## API 概览

所有 `/api/*` 接口（除 register / login / meta 外）均需在 Header 携带 `Authorization: Bearer <token>`。

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | /api/auth/register | 注册 | 公开 |
| POST | /api/auth/login | 登录，返回 token + user | 公开 |
| GET | /api/auth/me | 当前用户信息 | 登录 |
| GET | /api/meta | 分类 & 账户元数据 | 公开 |
| GET | /api/bills | 获取当前用户全部账单 | 登录 |
| GET | /api/bills/:id | 获取单条账单 | 登录 |
| POST | /api/bills | 新增账单 | 登录 |
| PUT | /api/bills/:id | 编辑账单 | 登录 |
| DELETE | /api/bills/:id | 删除账单 | 登录 |
| POST | /api/bills/query | 高级组合查询 | 登录 |
| GET | /api/stats/summary | 月/年/累计收支汇总 | 登录 |
| GET | /api/stats/12month | 近 12 月收支趋势 | 登录 |
| GET | /api/stats/expense-pie | 支出分类饼图 | 登录 |
| GET | /api/stats/income-pie | 收入来源饼图 | 登录 |
| GET | /api/stats/top5 | 支出 Top5 分类 | 登录 |
| GET | /api/stats/7day | 近 7 日收支趋势 | 登录 |
| GET | /api/stats/balance-trend | 资产结余曲线 | 登录 |
| GET | /api/stats/recent | 最近 10 条账单 | 登录 |
| POST | /api/transfer | 账户转账 | 登录 |
| GET | /api/excel/export | 导出 Excel | 登录 |
| POST | /api/excel/import | 导入 Excel（multipart） | 登录 |
| GET | /api/users | 用户列表 | 管理员 |
| POST | /api/users | 新增用户 | 管理员 |
| PUT | /api/users/:id | 编辑用户 | 管理员 |
| DELETE | /api/users/:id | 删除用户（不可删自己） | 管理员 |

## 切换 MySQL（生产部署）

编辑 `backend/config.py`，注释 SQLite 配置，取消 MySQL 注释：

```python
# SQLALCHEMY_DATABASE_URI = 'sqlite:///...'  # 注释掉
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:你的密码@localhost/bill_system'
```

需额外安装：`pip install pymysql`，并提前创建 `bill_system` 数据库。

## 版本

- **V2.0**（当前）：前后端分离重构，Vue 3 SPA + Flask REST API，SQLAlchemy ORM，SQLite 零配置开发
- V1.0：Flask + MySQL + Bootstrap + Jinja2 模板渲染（已归档）
