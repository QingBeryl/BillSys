## 项目名称
个人账单管理系统 BillSys

## 版本
**V1.0 稳定正式版**

# 一、 项目简介

个人记账系统是一款基于Flask + MySQL + Bootstrap + ECharts开发的全功能个人财务管理平台，采用MVC分层架构，实现了账单增删改查、多维度财务统计、可视化图表分析、用户认证等核心功能。本发布版已完成全部功能开发、Bug修复与体验优化，无已知问题，可直接部署使用，也可基于本版本进行二次开发扩展。

系统设计简洁易用，界面美观大方，全页面自适应，图表可视化效果专业，适合个人日常记账、课程设计、毕业设计，或作为全栈开发入门学习案例。

# 二、 后端技术栈

- 核心框架：Python Flask（轻量级Web框架，快速开发、易于扩展）。

- 数据库：MySQL（关系型数据库，稳定可靠，适合存储结构化账单数据）。

- 数据库连接：MySQLdb（Python连接MySQL的第三方库，高效稳定，适配MySQL 5.7/8.0）。

- 架构设计：MVC分层架构（Model模型层、View视图层、Controller控制层），代码逻辑清晰，便于维护和二次开发。

- 会话管理：Flask Session（用于用户登录状态保持，保障数据安全）。

# 三、 前端技术栈

- 页面布局：Bootstrap 5（响应式布局框架，快速构建美观、自适应的页面，减少CSS编写工作量）。

- 数据可视化：ECharts 5（百度开源可视化库，支持折线图、饼图、柱状图等多种图表，可视化效果专业，适配性强）。

- 基础技术：HTML5 + CSS3 + JavaScript（构建页面结构、样式与交互逻辑）。

- 模板渲染：Jinja2（Flask内置模板引擎，实现后端数据与前端页面的动态渲染，简化页面开发）。

# 四、 开发工具与环境

- 开发工具：PyCharm（Python开发首选，支持代码提示、调试，提升开发效率）、VS Code（可选，轻量级编辑器，适合快速修改代码）。

- 数据库工具：Navicat、MySQL Workbench（用于数据库表创建、数据管理、SQL语句执行）。

- 运行环境：Python 3.8+、MySQL 5.7/8.0、浏览器（Chrome推荐）。

# 五、 项目结构（发布版）

项目结构清晰，按MVC分层设计，便于开发者理解、维护和二次开发，具体结构如下：

```
BillSys/                          # 项目根目录
├── .venv/                        # 虚拟环境（发布时可忽略，部署时需重新创建）
├── models/                       # 模型层（MVC - Model）
│   ├── __init__.py               # 模型初始化文件
│   └── bill.py                   # 账单相关模型、数据库操作方法（核心）
├── templates/                    # 视图层（MVC - View）
│   ├── index.html                # 首页（核心页面，包含所有图表、统计卡片、最近账单）
│   ├── login.html                # 登录页面
│   ├── register.html             # 注册页面
│   └── bill/                     # 账单管理相关页面（新增、编辑、删除）
│       ├── add.html              # 新增账单页面
│       ├── edit.html             # 编辑账单页面
│       └── list.html             # 账单列表页面（可选，本版本首页已包含最近账单）
├── static/                       # 静态资源目录
│   ├── css/                      # CSS样式文件（Bootstrap样式、自定义样式）
│   ├── js/                       # JavaScript文件（自定义交互逻辑，本版本核心JS在index.html中）
│   └── images/                   # 图片资源（可选，用于页面美化）
├── app.py                        # 控制层（MVC - Controller），项目入口文件，路由配置
├── requirements.txt              # 项目依赖包列表（部署时需安装）
├── db.sql                        # 数据库脚本（用于创建数据表，发布版已包含完整表结构）
└── README.md                     # 项目说明文档（本文件）
```
# 六、 模型层（models/bill.py

模型层负责数据库操作，封装了账单管理、数据统计、图表数据获取等核心方法，所有方法均做了异常处理和容错处理，确保数据库操作稳定，具体核心方法如下：

1. get_12month_data(user_id)：获取用户近12个月的收支数据，返回按月份排序的收入、支出统计结果，用于“所有收支趋势折线图”渲染；无数据时自动返回示例数据，避免图表空白。

2. get_income_pie(user_id)：获取用户收入二级分类统计数据，返回二级分类名称及对应收入总额，用于“收入分类饼图”渲染；无数据时自动返回示例数据。

3. get_top5_spend(user_id)：获取用户支出Top5分类数据，按支出金额从高到低排序，返回前5个分类及对应支出总额，用于“支出Top5排行柱状图”渲染；无数据时自动返回示例数据。

4. get_7day_data(user_id)：获取用户近7天的每日收支数据，返回按日期排序的每日收入、支出统计结果，用于“近7天每日收支趋势图”渲染；无数据时自动返回示例数据。

5. get_balance_trend(user_id)：获取用户每日资产结余趋势数据，按日期累计计算结余金额，返回日期及对应结余，用于“每日资产结余趋势曲线图”渲染；无数据时自动返回示例数据。

6. 其他方法：账单新增（add_bill）、编辑（edit_bill）、删除（delete_bill）、查询（get_bill_by_id）等基础方法，实现账单全生命周期管理。

# 七、 控制层（app.py）

控制层负责路由配置、请求处理、数据传递，连接模型层与视图层，具体核心路由如下：

1. /：首页路由，请求时调用模型层所有图表数据、统计数据，传递给index.html模板，渲染首页所有内容。

2. /login：登录路由，处理用户登录请求，验证账号密码，创建Session会话。

3. /register：注册路由，处理用户注册请求，将用户信息插入数据库，完成注册。

4. /bill/add：新增账单路由，处理新增账单请求，将账单数据插入数据库，跳转回首页。

5. /bill/edit/<id>：编辑账单路由，根据账单ID查询账单信息，渲染编辑页面，处理编辑请求。

6. /bill/delete/<id>：删除账单路由，根据账单ID删除账单数据，跳转回首页。

7. /logout：退出登录路由，销毁Session会话，跳转至登录页面。

# 八、 视图层（templates目录）

视图层负责页面渲染，采用Jinja2模板引擎，结合Bootstrap 5实现页面布局，核心页面说明如下：

1. index.html：首页，核心页面，包含6大图表、财务统计卡片、最近账单列表，所有图表JS均在本页面中，已优化适配，无空白、无报错。

2. login.html：登录页面，简洁的登录表单，支持账号密码输入、登录提交，验证失败提示错误信息。

3. register.html：注册页面，支持用户名、密码输入，注册成功跳转至登录页面，用户名重复提示错误信息。

4. bill/add.html：新增账单页面，表单包含收支类型、分类、金额、日期、备注等字段，提交后跳转回首页。

5. bill/edit.html：编辑账单页面，表单自动填充原有账单信息，修改后提交，跳转回首页。

# 九、 图表渲染核心逻辑（index.html）

所有图表均在index.html中渲染，采用ECharts 5开发，核心逻辑如下：

- 图表初始化：等待页面完全加载（window.onload）后初始化所有图表，避免DOM未渲染完成导致的图表空白问题。

- 数据传递：通过Jinja2模板渲染，将后端传递的图表数据（month12、pie、in_pie等）注入前端JS，实现数据动态渲染。

- 图表配置：每个图表均设置了标题、坐标轴、系列样式，收入与支出采用不同颜色区分，折线图上下分层，饼图采用环形设计，柱状图排序清晰。

- 自适应处理：监听浏览器窗口缩放事件，调用resize()方法，实现图表自动重绘，适配不同窗口尺寸。

- 容错处理：后端已做空数据兜底，前端无需额外处理，确保图表永远不会空白。

# 十、 部署运行步骤（发布版，详细可操作）

本发布版可直接部署运行，无需额外开发，步骤如下（以Windows系统为例，macOS、Linux步骤类似）：

# 十一、 环境准备

1. 安装Python：下载并安装Python 3.8+（推荐3.8），安装时勾选“Add Python to PATH”，确保环境变量配置成功。

2. 安装MySQL：下载并安装MySQL 5.7或8.0，记住MySQL的root账号密码（部署时需用到），确保MySQL服务正常运行。

3. 安装开发/部署工具：推荐安装PyCharm（用于打开项目、运行代码）或VS Code，以及Navicat（用于执行数据库脚本）。

# 十二、 项目部署

1. 下载项目：将个人记账系统发布版项目文件解压至本地（如D:\Programming\BillSys）。

2. 创建虚拟环境（可选，推荐）：
        

  - 打开命令提示符（CMD），进入项目根目录：cd D:\Programming\BillSys

  - 创建虚拟环境：python -m venv .venv

  - 激活虚拟环境：.venv\Scripts\activate（Windows）；source .venv/bin/activate（macOS/Linux）

3. 安装依赖包：激活虚拟环境后，执行命令：pip install -r requirements.txt，等待依赖包安装完成（若安装失败，可单独安装：pip install flask mysqldb）。

4. 导入数据库脚本：
        

  - 打开Navicat，连接本地MySQL，创建数据库（数据库名：billsys，编码：utf8mb4）。

  - 右键点击创建的billsys数据库，选择“运行SQL文件”，选择项目根目录下的db.sql文件，执行SQL脚本，创建数据表（users表、bills表）。

  - 或运行下方代码
```sql
CREATE DATABASE bill_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE bill_system;

-- 用户表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    is_admin TINYINT DEFAULT 0
);

-- 初始管理员账号：admin 123456
INSERT INTO users(username,password,is_admin) VALUES('admin','123456',1);

-- 账单表
CREATE TABLE bills (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    bill_date DATETIME NOT NULL,
    type VARCHAR(10) NOT NULL, -- 收入/支出
    money DECIMAL(10,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL,
    account VARCHAR(50) NOT NULL,
    book_name VARCHAR(50) DEFAULT '日常账本',
    refund DECIMAL(10,2) DEFAULT 0.00,
    remark TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

5. 修改数据库配置：打开项目根目录下的app.py文件，找到MySQL连接配置代码，修改为自己的MySQL账号密码：
        mysql = MySQL(app, host='localhost', user='root', password='你的MySQL密码', database='billsys', port=3306)

6. 运行项目：
        

  - 在PyCharm中打开项目，设置虚拟环境为项目创建的.venv，点击运行app.py（或在CMD中执行：python app.py）。

  - 运行成功后，控制台会提示：* Running on http://127.0.0.1:5000/（Press CTRL+C to quit）。

7. 访问系统：打开浏览器，输入http://127.0.0.1:5000/，进入登录页面，注册账号后即可登录使用。

# 十三、 部署注意事项

- MySQL服务必须正常运行，否则无法连接数据库，项目启动失败。

- 数据库配置中的账号密码必须正确，否则会出现数据库连接错误。

- 依赖包必须全部安装完成，若MySQLdb安装失败，可尝试安装pymysql，并用pymysql替换MySQLdb（修改app.py中的导入和连接代码）。

- 项目运行时，请勿关闭CMD窗口或PyCharm的运行控制台，否则项目会停止运行。

- 若浏览器访问时出现404错误，检查路由配置是否正确，或项目是否正常启动。

# 十四、 常见问题与解决方案（发布版）

常见问题

解决方案

项目启动失败，提示“MySQLdb not found”

1. 执行pip install mysqldb；2. 若安装失败，安装pymysql（pip install pymysql），并在app.py中修改：import pymysql，pymysql.install_as_MySQLdb()，重新运行。

数据库连接失败，提示“Access denied for user 'root'@'localhost'”

检查app.py中的MySQL密码是否正确，确保MySQL root账号密码无误，且MySQL服务正常运行。

首页图表空白，无任何显示

1. 检查后端方法是否正确替换为发布版的5个图表方法；2. 检查index.html中的JS是否替换为发布版JS；3. 清除浏览器缓存，重新刷新页面。

账单新增后，图表未同步更新

检查账单新增方法是否正确调用，新增后是否跳转回首页；若未同步，手动刷新首页即可。

页面布局错乱，自适应失效

检查Bootstrap 5是否正常加载，确保页面中引入了Bootstrap的CSS和JS文件；若仍有问题，清除浏览器缓存后重试。

用户注册后，无法登录

检查注册方法是否将用户信息插入users表，登录时输入的账号密码是否与注册时一致；可通过Navicat查看users表，确认用户信息是否存在。

# 十五、 二次开发指南（发布版）

本发布版代码分层清晰、逻辑规范，支持二次开发扩展，以下是常见的二次开发方向及指南：

# 功能扩展方向

- 账单导出Excel：集成openpyxl库，新增导出路由，将用户账单数据导出为Excel文件。

- 预算设置与超支提醒：新增预算表，用户设置月度/年度预算，当支出超过预算时，给出提醒。

- 账单搜索与筛选：新增搜索框，支持按日期、分类、金额范围筛选账单。

- 暗黑模式：新增主题切换功能，支持浅色/暗黑模式切换，优化夜间使用体验。

- 手机端适配：优化页面样式，适配手机端屏幕，新增移动端适配布局。

- 密码重置：新增密码重置功能，支持用户通过邮箱/手机验证码重置密码。

# 二次开发注意事项

- 二次开发前，建议备份原有项目文件，避免修改错误导致项目无法运行。

- 新增功能时，遵循MVC分层架构，新增模型方法放在models目录，新增路由放在app.py，新增页面放在templates目录。

- 修改图表相关功能时，注意保持数据格式与前端JS的适配，避免出现图表空白、数据错乱。

- 新增依赖包时，需将依赖包名称及版本添加到requirements.txt中，便于后续部署。

- 修改数据库相关操作时，需先备份数据库，避免数据丢失；新增数据表时，需更新db.sql脚本。

# 十六、 其它
# 版本说明（发布版）

- 版本号：V1.0.0（发布版）

- 发布日期：2026年5月

- 版本特性：功能完整、无Bug、图表全部正常渲染、空数据兜底、自适应布局、多用户隔离。

- 更新日志：
        

  - V1.0.0（发布版）：完成全部核心功能开发，修复所有已知Bug，优化图表适配，添加空数据兜底，完善用户体验。

# 免责声明

本个人记账系统（发布版）仅供个人使用、学习交流、课程设计、毕业设计使用，请勿用于商业用途。开发者不对项目的安全性、稳定性做任何商业承诺，若因使用本项目导致的任何数据丢失、安全问题，开发者不承担任何责任。

本项目开源，欢迎开发者基于本版本进行二次开发、优化，但请保留原作者相关信息，尊重开源精神。

# 补充说明

若在部署、使用、二次开发过程中遇到问题，可参考本README中的“常见问题与解决方案”，若仍无法解决，可根据实际问题排查代码，或联系开发者寻求帮助。

本发布版已完成全部优化，无任何已知问题，可直接用于个人使用或课程设计，祝使用愉快！