import sqlite3
from sqlite3 import Error

def test_connection():
    """ 测试数据库连接 """
    conn = sqlite3.connect('test.db')
    print ("数据库打开成功")
    c = conn.cursor()

def create_connection():
    """ 创建数据库连接 """
    conn = None
    try:
        conn = sqlite3.connect('project_data.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Error as e:
        print(e)
    return conn


def create_tables():
    """ 创建数据库表 """
    conn = create_connection()
    if conn is not None:
        # 创建资源表
        create_resources_table = ''' CREATE TABLE IF NOT EXISTS resources (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            name TEXT NOT NULL,
                                            remark TEXT,
                                            unit TEXT NOT NULL,
                                            cost_price REAL NOT NULL,
                                            sale_price REAL NOT NULL
                                        ); '''
        # 创建项目表
        create_projects_table = ''' CREATE TABLE IF NOT EXISTS projects (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            name TEXT NOT NULL,
                                            project_date TEXT NOT NULL
                                        ); '''
        # 创建项目分组表
        create_project_groups_table = ''' CREATE TABLE IF NOT EXISTS project_groups (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            project_id INTEGER NOT NULL,
                                            name TEXT NOT NULL,
                                            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
                                        ); '''
        # 创建项目分组资源表
        create_project_group_resources_table = ''' CREATE TABLE IF NOT EXISTS project_group_resources (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            group_id INTEGER NOT NULL,
                                            resource_id INTEGER NOT NULL,
                                            quantity INTEGER NOT NULL DEFAULT 1,
                                            FOREIGN KEY (group_id) REFERENCES project_groups (id) ON DELETE CASCADE,
                                            FOREIGN KEY (resource_id) REFERENCES resources (id) ON DELETE CASCADE
                                        ); '''
        # 创建报价表（修改为关联项目ID）
        create_quotations_table = ''' CREATE TABLE IF NOT EXISTS quotations (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            project_id INTEGER,
                                            project_name TEXT NOT NULL,
                                            quote_date TEXT NOT NULL,
                                            total_cost REAL NOT NULL DEFAULT 0,
                                            total_sale REAL NOT NULL DEFAULT 0,
                                            profit REAL NOT NULL DEFAULT 0,
                                            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE SET NULL
                                        ); '''
        # 创建报价资源项表
        create_quotation_items_table = ''' CREATE TABLE IF NOT EXISTS quotation_items (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            quotation_id INTEGER NOT NULL,
                                            resource_id INTEGER NOT NULL,
                                            quantity INTEGER NOT NULL DEFAULT 1,
                                            FOREIGN KEY (quotation_id) REFERENCES quotations (id) ON DELETE CASCADE,
                                            FOREIGN KEY (resource_id) REFERENCES resources (id) ON DELETE CASCADE
                                        ); '''
        # 创建批量记录表（用于存储project_data）
        create_batch_record_table = ''' CREATE TABLE IF NOT EXISTS BATCH_RECORD (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            date TEXT NOT NULL,
                                            content TEXT NOT NULL,
                                            quantity INTEGER NOT NULL,
                                            unit_price REAL NOT NULL,
                                            size TEXT,
                                            material TEXT,
                                            subtotal REAL NOT NULL
                                        ); '''
        try:
            c = conn.cursor()
            c.execute(create_resources_table)
            c.execute(create_projects_table)
            c.execute(create_project_groups_table)
            c.execute(create_project_group_resources_table)
            c.execute(create_quotations_table)
            c.execute(create_quotation_items_table)
            c.execute(create_batch_record_table)
            conn.commit()
            print("Tables created successfully")
        except Error as e:
            print(e)
        finally:
            conn.close()
    else:
        print("Error! Cannot create the database connection.")

def insert_project_data():
    """ 将project_data示例数据插入到BATCH_RECORD表中 """
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            # 检查BATCH_RECORD表是否为空
            c.execute("SELECT COUNT(*) FROM BATCH_RECORD")
            count = c.fetchone()[0]
            
            if count == 0:
                # 插入project_data中的数据
                sql = ''' INSERT INTO BATCH_RECORD (date, content, quantity, unit_price, size, material, subtotal)
                          VALUES (?, ?, ?, ?, ?, ?, ?) '''
                
                for item in project_data:
                    # 注意：project_data中的数据顺序是 (date, content, quantity, unit_price, size, material, subtotal)
                    c.execute(sql, item)
                
                conn.commit()
                print(f"成功插入 {len(project_data)} 条数据到BATCH_RECORD表")
            else:
                print(f"BATCH_RECORD表中已有 {count} 条数据，跳过插入")
        except Error as e:
            print(e)
        finally:
            conn.close()
    else:
        print("Error! Cannot create the database connection.")

def select_data(query, params=()):
    """ 执行SELECT查询 
    输入语法：query - SQL查询语句，params - 查询参数（可选）
    输出语法：返回查询结果列表，每个结果为一个字典
    """
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(query, params)
            rows = c.fetchall()
            return [dict(row) for row in rows]
        except Error as e:
            print(e)
            return ["查询出错"]
        finally:
            conn.close()
    else:
        print("Error! Cannot create the database connection.")
        return ["查询出错"]



# def select_data(condition=None, fields='*'):
#     """
#     查询批量数据函数
#     :param condition: 查询条件（SQL WHERE 子句，例如 "date='2026-02-13'"），None 表示查询所有
#     :param fields: 要查询的字段（例如 "date,content,subtotal"），默认 '*' 查询所有字段
#     :return: 查询结果列表（每个元素是一行数据的元组）
#     """
#     # 连接数据库
#     conn = sqlite3.connect('project_data.db')
#     c = conn.cursor()
    
#     # 构建查询SQL
#     if condition:
#         sql = f"SELECT {fields} FROM BATCH_RECORD WHERE {condition}"
#     else:
#         sql = f"SELECT {fields} FROM BATCH_RECORD"
    
#     try:
#         # 执行查询
#         cursor = c.execute(sql)
#         # 获取所有查询结果
#         results = cursor.fetchall()
        
#         # 打印查询结果（格式化输出）
#         print("="*80)
#         print(f"查询条件: {condition if condition else '无（查询所有）'}")
#         print(f"查询字段: {fields}")
#         print("查询结果:")
#         print("-"*80)
        
#         # 定义字段名映射（用于表头显示）
#         field_names = {
#             'date': '日期',
#             'content': '内容',
#             'quantity': '数量',
#             'unit_price': '单价',
#             'size': '尺寸',
#             'material': '材料',
#             'subtotal': '小计'
#         }
        
#         # 打印表头（如果查询所有字段）
#         if fields == '*':
#             print(f"{'日期':<12} {'内容':<30} {'数量':<6} {'单价':<8} {'尺寸':<12} {'材料':<20} {'小计':<8}")
#             print("-"*80)
#             # 打印每行数据
#             for row in results:
#                 print(f"{row[0]:<12} {row[1]:<30} {row[2]:<6} {row[3]:<8.2f} {row[4]:<12} {row[5]:<20} {row[6]:<8.2f}")
#         else:
#             # 自定义字段的打印
#             field_list = fields.split(',')
#             # 打印自定义表头
#             header = ""
#             for f in field_list:
#                 f = f.strip()
#                 header += f"{field_names.get(f, f):<15} "
#             print(header)
#             print("-"*80)
#             # 打印自定义字段数据
#             for row in results:
#                 row_str = ""
#                 for idx, val in enumerate(row):
#                     if isinstance(val, (int, float)):
#                         row_str += f"{val:<15.2f}"
#                     else:
#                         row_str += f"{val:<15}"
#                 print(row_str)
        
#         print("="*80)
#         print(f"共查询到 {len(results)} 条数据")
        
#         return results
    
#     except sqlite3.Error as e:
#         print(f"查询出错: {e}")
#         return ["查询出错"]
#     finally:
#         # 关闭数据库连接
#         conn.close()

# def select_data(query, params=()):
#     """ 执行SELECT查询 
#     输入语法：query - SQL查询语句，params - 查询参数（可选）
#     输出语法：返回查询结果列表，每个结果为一个字典
#     """
#     conn = create_connection()
#     if conn is not None:
#         try:
#             c = conn.cursor()
#             c.execute(query, params)
#             rows = c.fetchall()
#             return [dict(row) for row in rows]
#         except Error as e:
#             print(e)
#             return []
#         finally:
#             conn.close()
#     else:
#         print("Error! Cannot create the database connection.")
#         return []


# -------------------------- 批量数据模板 --------------------------
# 格式：[日期, 内容, 数量, 单价, 尺寸, 材料, 小计]
project_data = [
    
    ('2026-02-13', '美丽客厅开放时间牌', 1, 400, '50*30厘米', '不锈钢+安装', 400),
    ('2026-02-13', '开放时间（前门入口）', 1, 400, '50*30厘米', '不锈钢+安装', 400),
    ('2026-02-14', '湿地公园开放时间（后门入口）', 1, 130, '80*60厘米', '加厚PVC板+UV+安装', 130),
    ('2026-01-08', '宣传栏新院第2024年第1期', 1, 150, '2.5*1.2米', '喷画+安装', 150),
    ('2026-01-08', '创文明镇禁烟标语', 30, 20, '30*40厘米', '喷画裱KT板', 600),
    ('2026-01-10', '未成年人制度、肠道门诊制度', 14, 45, '50*70厘米', '喷画裱KT板', 630),
    ('2026-02-15', '大型标识牌制作', 1, 500, '70*50厘米', '不锈钢牌UV内容+安装', 500),
    ('2026-02-16', '消防安全出口标识', 8, 35, '20*40厘米', '亚克力板+丝印', 280),
    ('2026-02-17', '科室门牌（10个科室）', 10, 85, '15*30厘米', '铝合金+蚀刻', 850),
    ('2026-02-18', '户外宣传海报', 5, 220, '1.2*1.8米', '户外喷绘+安装', 1100)
]

if __name__ == '__main__':
    create_tables()
    insert_project_data()