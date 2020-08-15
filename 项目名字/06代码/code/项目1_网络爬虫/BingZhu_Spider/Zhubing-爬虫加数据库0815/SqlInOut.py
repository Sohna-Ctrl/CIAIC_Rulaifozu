# -*- encoding:utf-8 -*-
# -*- encoding:utf-8 -*-
# @Time : ${08} ${14}
# @Author : 朱冰
# @Site : ${Xi‘an}
# @File : ${What to by}.py
# @Software: ${PRODUCT_NAME

import pymysql
import traceback

#
# # 仅使用数据库进行两种操作：第一使用数据库创建表格，第二使用数据库存储爬虫爬下来的list中的内容
#
# #
# def fun_creattableInsql():
#     try:
#         var_connection = pymysql.connect(host='localhost', port=3306, user='zhubingSpiderWeb', password='zhubingSpiderWeb',
#                                          database='db_python06_01',
#                                          charset='utf8')
#         print(var_connection)
#         # 获取数据库操作对象 游标
#         var_cursor = var_connection.cursor()
#
# #         # 通过游标操作数据库
#         var_sql = '''
# 			CREATE TABLE t_original_Cosmetics_03(
#
# 				cosmetics_name VARCHAR(200)  PRIMARY KEY,
# 				cosmetics_price VARCHAR(200),
# 				cosmetics_link VARCHAR(200)
# 			)
# 		'''
#         var_result = var_cursor.execute(var_sql)
#         print('执行结果为：', var_result, '。')
#     except Exception as e:
#         traceback.print_exc()
#     finally:
#         # 关闭
#         var_cursor.close()
#         var_connection.close()
#         pass
#     pass
# # 创建第一个工作表
# fun_creattableInsql()


def fun_insert_method(var_list_data):
    var_connection = pymysql.connect(host='localhost', port=3306, user='zhubingSpiderWeb', password='zhubingSpiderWeb',
                                     database='db_python06_01',
                                     charset='utf8')

    print('数据库连接对象：', var_connection)
    var_cursor = var_connection.cursor()
    # var_cursor.execute("delete from t_original_Cosmetics")
    var_sql = "insert  into `t_original_Cosmetics_03`(cosmetics_name,cosmetics_price,cosmetics_link) values(%s,%s,%s)"
    # 创建游标对象
    # var_cursor = var_connection.cursor()
    # 步骤3;服务器端自动执行sql，把执行结果返回
    var_result = var_cursor.execute(var_sql, var_list_data)

    print('mysql服务器端返回的内容：', var_result)
    var_connection.commit()

    var_cursor.close()  # 关闭连接
    var_connection.close()
    pass


['克丽丝汀迪奥迪奥小姐花漾淡香氛', '￥570.00~￥1195.00', 'https://www.sephora.cn/product/1134.html']