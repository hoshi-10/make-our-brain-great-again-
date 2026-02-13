from flask import Flask
from flask_cors import CORS
from routes import api_bp
from database import create_tables, select_data, insert_project_data

# 初始化Flask应用
app = Flask(__name__)

# 配置CORS，允许所有来源的请求
CORS(app)

# 注册API蓝图
app.register_blueprint(api_bp, url_prefix='/api')

# 初始化数据库表
create_tables()
# 插入示例数据
insert_project_data()

@app.route('/database')
def database():
    """数据库路由，测试数据库连接和查询"""
    data = select_data("SELECT * FROM BATCH_RECORD")
    return f"Database data: {data}"

@app.route('/quotations')
def quotations():
    """查询报价表数据"""
    data = select_data("SELECT * FROM quotations")
    return f"Quotations data: {data}"


@app.route('/')
def index():
    """ 根路由 """
    return "Quotation Management System API is running"

@app.route('/user/<int:user_id>')
def user_profile(user_id):
    """用户路由"""
    return f'User ID: {user_id}'


if __name__ == '__main__':
    # 启动Flask应用，监听所有网络接口，端口5000
<<<<<<< HEAD
    app.run(host='0.0.0.0', port=5000, debug=True)
=======
    app.run(host='0.0.0.0', port=5000, debug=True)
>>>>>>> 213ebc7712615de7509a32fb70346d9b024780a1
