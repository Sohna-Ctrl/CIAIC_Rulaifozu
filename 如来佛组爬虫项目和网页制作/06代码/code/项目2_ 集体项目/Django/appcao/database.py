# -*- encoding:utf-8 -*-
# @Time : ${20/08/11} ${18:00}
# @Author : 曹梓
# @Site : ${https://www.duitang.com/album/?id=98243426&spm=2014.12553688.202.0}
# @File : ${database}.py
# @Software: ${PyCharm}

import pymysql
import traceback
import logging

'''
描述：把数据保存到表里
入参：list容器，list容器里的元素是字段里的值
'''


# 表格操作数据库连接
def fun_connect_method(logger):
	"""
	建立表格数据库与python的连接
	:param var_connection:
	:param logger: 打印日志的对象，通过“.”可打印不同级别的日志
	:return: 连接
	"""
	logger.debug("表格操作数据库连接开始执行！")
	try:
		var_connection = pymysql.connect(host='localhost', port=3306, user='zcao', password='mima',
										 database='db_photo',
										 charset='utf8')
		logger.info("表格操作数据库连接成功！")
		return var_connection
	except:
		traceback.print_exc()
		logger.error("表格操作数据库连接错误！")
	logger.debug("表格操作数据库连接执行完毕！")
	pass


# 表格操作数据库连接关闭
def fun_connect_close_method(var_connection, logger):
	"""
		关闭表格数据库与python的连接
		:param var_connection: 连接
		:param logger: 打印日志的对象，通过“.”可打印不同级别的日志
		:return: 无返回值
		"""
	logger.debug("关闭表格操作数据库连接开始执行！")
	try:
		var_connection.close()
		logger.info("关闭表格操作数据库连接成功！")
	except:
		traceback.print_exc()
		logger.error("关闭表格操作数据库连接错误！")
	logger.debug("关闭表格操作数据库连接执行完毕！")
	pass


#  执行创建表格
def fun_create_method(var_connection, logger):
	"""
	在数据库创建一个表格
	:param logger: 打印日志的对象，通过“.”可打印不同级别的日志
	:return: 无返回值
	"""
	logger.debug("创建表格操作开始执行！")
	try:

		logger.info('创建表格操作数据库连接对象：%s' % var_connection)
		# 获取数据库操作对象 游标
		var_cursor = var_connection.cursor()

		# 通过游标操作数据库
		# 若表格已存在删除表格
		var_sql = '''
			DROP TABLE IF EXISTS t_photo
				'''
		var_cursor.execute(var_sql)
		logger.debug("若表格已存在则删除表格！")
		# 通过游标操作数据库创建表格
		var_sql = '''
			CREATE TABLE t_photo(
				photo_id INT PRIMARY KEY AUTO_INCREMENT,
				photo_directory VARCHAR(100),
				photo_name VARCHAR(100),
				photo_url VARCHAR(100)
			)
		'''
		var_result = var_cursor.execute(var_sql)
		logger.info('创建表格操作执行结果为：%s' % var_result)
	except Exception as e:
		traceback.print_exc()
		logger.error("创建表格操作错误！")
	finally:
		# 关闭
		var_cursor.close()
		pass
	logger.debug("创建表格操作执行完毕！")
	pass


# 插入操作
def fun_insert_method(var_connection, var_list_data, logger):
	"""
	在数据库中的表格中插入信息
	:param var_list_data:
	:param logger: 打印日志的对象，通过“.”可打印不同级别的日志
	:return: 无返回值
	"""
	logger.debug("插入操作开始执行！")
	try:
		# 步骤1：python代码连接到服务器端

		logger.info('插入操作数据库连接对象：%s' % var_connection)

		# 步骤2：把sql语句发送给服务器
		#  创建sql
		var_sql = "insert  into `t_photo`(photo_directory,photo_name,photo_url) values(%s,%s,%s)"
		# 创建游标对象
		var_cursor = var_connection.cursor()

		# 步骤3;服务器端自动执行sql，把执行结果返回
		var_result = var_cursor.execute(var_sql, var_list_data)
		logger.info('插入操作执行结果为：%s' % var_result)
		var_connection.commit()
	except Exception as e:
		traceback.print_exc()
		logger.error("插入操作错误！")
	finally:
		# 步骤4：关闭连接
		var_cursor.close()
	logger.debug("插入操作执行完毕！")
	pass


# 查询操作
def fun_search_method(var_connection, str, logger):
	"""
	在数据库中的表格中查询信息
	:param str: 查询某信息的字符
	:param logger: 打印日志的对象，通过“.”可打印不同级别的日志
	:return: 无返回值
	"""
	logger.debug("查询操作开始执行！")
	try:

		logger.info('查询操作数据库连接对象：%s' % var_connection)
		# 获取数据库操作对象 游标
		var_cursor = var_connection.cursor()

		# 通过游标操作数据库
		var_sql = "select photo_id,photo_directory,photo_name,photo_url  from t_photo where photo_id=%s or photo_directory=%s or photo_name=%s or photo_url=%s"
		var_cursor.execute(var_sql, (str, str, str, str,))
		# list容器，list容器里的元素是一个list
		var_result = var_cursor.fetchall()

		for element in var_result:
			logger.info('查询操作执行结果为：%s %s %s %s' % element)
			# print(element[0], element[1], element[2], element[3])
			pass
	except Exception as e:
		traceback.print_exc()
		logger.error("查询操作错误！")
	finally:
		# 关闭
		var_cursor.close()
		pass
	logger.debug("查询操作执行完毕！")
	pass


# 删除操作
def fun_delete_method(var_connection, str, logger):
	"""
	在数据库中的表格中删除信息
	:param str: 删除某信息的字符
	:param logger: 打印日志的对象，通过“.”可打印不同级别的日志
	:return: 无返回值
	"""
	logger.debug("删除操作开始执行！")
	try:

		logger.info('删除操作数据库连接对象：%s' % var_connection)
		# 获取数据库操作对象 游标
		var_cursor = var_connection.cursor()

		# 通过游标操作数据库
		var_sql = '''
				DELETE FROM t_photo
				WHERE photo_id=%s or photo_directory=%s or photo_name=%s or photo_url=%s
		'''
		var_result = var_cursor.execute(var_sql, (str, str, str, str,))
		logger.info('删除操作执行结果为：%s' % var_result)
		var_connection.commit()
	except Exception as e:
		traceback.print_exc()
		logger.error("删除操作错误！")
	finally:
		# 关闭
		var_cursor.close()
		pass
	logger.debug("删除操作执行完毕！")
	pass


# 更新操作
def fun_update_method(var_connection, str_1, str_2, str_3, str_4, logger):
	"""
	在数据库中的表格中更新信息
	:param str_1: 删除某信息的字符，字段 photo_id
	:param str_2: 删除某信息的字符，字段 photo_directory
	:param str_3: 删除某信息的字符，字段 photo_name
	:param str_4: 删除某信息的字符，字段 photo_url
	:param logger: 打印日志的对象，通过“.”可打印不同级别的日志
	:return: 无返回值
	"""
	logger.debug("更新操作开始执行！")
	try:
		logger.info('更新操作数据库连接对象：%s' % var_connection)
		# 获取数据库操作对象 游标
		var_cursor = var_connection.cursor()

		# 通过游标操作数据库
		var_sql = '''
			UPDATE t_photo
			SET photo_directory = %s, photo_name = %s, photo_url = %s
			WHERE photo_id=%s;
		'''
		var_result = var_cursor.execute(var_sql, (str_2, str_3, str_4, str_1))
		logger.info('更新操作执行结果为：%s' % var_result)
		var_connection.commit()
	except Exception as e:
		traceback.print_exc()
		logger.error("更新操作错误！")
	finally:
		# 关闭
		var_cursor.close()
	logger.debug("更新操作执行完毕！")
	pass


def get_logger():
	"""
	日志对象、打印级别和输出端口等配置
	:return: 打印对象
	"""
	# 日志对象
	logger = logging.getLogger()

	# file_log 写入文件配置
	# 日志的格式
	formatter = logging.Formatter('%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
	# 日志文件路径文件名称，编码格式
	fh = logging.FileHandler(r'logger.log', encoding='utf-8')
	# 日志打印级别
	fh.setLevel(logging.DEBUG)
	fh.setFormatter(formatter)
	logger.addHandler(fh)

	# console log 控制台输出控制
	# ch = logging.StreamHandler(sys.stdout)
	# ch.setLevel(logging.DEBUG)
	# ch.setFormatter(formatter)
	# logger.addHandler(ch)

	# 输出日志
	stream_handler = logging.StreamHandler()
	stream_handler.setFormatter(formatter)
	logger.addHandler(stream_handler)
	logger.setLevel(logging.DEBUG)
	return logger
	pass


if __name__ == '__main__':
	# 创建日志对象
	# logger = get_logger()
	pass

