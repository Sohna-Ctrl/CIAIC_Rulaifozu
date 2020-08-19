import traceback						# 异常处理
import logging                          # 为程序添加日志

''''
描述：把数据保存到表里
入参：list容器，list容器里的元素是字段里的值

'''


def fun_setup_method(var_connection):
	'''
	执行创建表格
	:param var_connection: 连接服务器
	:return: 无
	'''
	try:
		# 获取数据库操作对象 游标
		var_cursor = var_connection.cursor()

		# 判断表格是否存在，如果存在，删除表格，重新创建
		var_sql = '''drop table if exists t_music'''
		var_cursor.execute(var_sql)

		# 通过游标操作数据库
		var_sql = '''
			CREATE TABLE t_music(
				music_id INT PRIMARY KEY AUTO_INCREMENT,
				song_name VARCHAR(200),
				song_url VARCHAR(500),
				artist_name VARCHAR(500),
				artist_url VARCHAR(500),
				album_name VARCHAR(500),
				album_url VARCHAR(500),
				pic_url VARCHAR(500)
			)
		'''

		# 创建表格
		var_cursor.execute(var_sql)
		#logger.info("创建数据库成功，并新建了一个表格")
	except Exception as e:
		traceback.print_exc()
		#logger.error("创建表格失败！")
	finally:
		# 关闭游标
		var_cursor.close()
		pass
	pass


def fun_insert_method(var_list_data,var_connection):
	'''
	插入数据
	:param var_list_data: 爬取的数据
	:param var_connection: 连接服务器
	:return: 无
	'''
	try:
		# 把sql语句发送给服务器
		#  创建sql
		var_sql = "insert  into `t_music`(song_name ,song_url,artist_name ,artist_url ,album_name ,album_url ,pic_url) values(%s,%s,%s,%s,%s,%s,%s)"
		# 创建游标对象
		var_cursor = var_connection.cursor()

		# 步骤3;服务器端自动执行sql，把执行结果返回
		var_cursor.execute(var_sql, var_list_data)
		var_connection.commit()
		logger.info("成功将数据插入表格！")
	except Exception as e:
			traceback.print_exc()
	finally:
		# 关闭游标
		var_cursor.close()
		pass
	pass


def fun_search_method(p1,var_connection):
	'''
	查询操作
	:param p1: documentary_id
	:param var_connection: 连接服务器
	:return: 无
	'''
	try:
		# 获取数据库操作对象 游标
		var_cursor = var_connection.cursor()

		# 通过游标操作数据库
		var_sql = "select music_id,song_name ,song_url,artist_name ,artist_url ,album_name ,album_url ,pic_url  from t_music where music_id>%s"
		var_cursor.execute(var_sql, (p1,))

		# list容器，list容器里的元素是一个list
		var_result = var_cursor.fetchall()
		for element in var_result:
			logger.info("查询成功：")
			logger.info("%s,%s,%s,%s,%s,%s,%s,%s",element[0], element[1], element[2],element[3],element[4], element[5],element[6],element[7])
			pass
	except Exception as e:
		traceback.print_exc()
	finally:
		# 关闭
		var_cursor.close()
		pass
	pass


def fun_delete_method(str1, str2, var_connection):
	'''
	删除操作
	:param str1: documentary_id
	:param str2: documentary_name
	:param var_connection: 连接服务器
	:return: 无
	'''
	try:
		# 获取数据库操作对象 游标
		var_cursor = var_connection.cursor()
		# 通过游标操作数据库
		var_sql = "DELETE FROM t_music WHERE music_id=%s AND music_name = %s"
		var_result = var_cursor.execute(var_sql,(str1,str2,))
		print('mysql服务器端返回的内容：', var_result)
		var_connection.commit()
	except Exception as e:
		traceback.print_exc()
	finally:
		# 关闭连接
		var_cursor.close()
		pass


def fun_close_database(var_connection):
	'''
	关闭数据库
	:param var_connection:连接服务器
	:return:无
	'''
	var_connection.close()
	pass


# 为程序添加日志
def get_logger():
    """
    日志对象、打印级别和输出端口等配置
    :return: 日志对象
    """
    # 日志对象
    logger = logging.getLogger()
    # file_log 写入文件配置
    # 日志的格式
    formatter = logging.Formatter('%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    # 日志文件路径文件名称，编码格式
    fh = logging.FileHandler(r'test_logger.log', encoding='utf-8')
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
	# 打印日志的初始配置
	logger = get_logger()
	pass
