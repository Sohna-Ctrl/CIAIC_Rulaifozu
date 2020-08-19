# -*- encoding:utf-8 -*-
# @Time : ${20/08/08} ${18:00}
# @Author : 曹梓
# @Site : ${https://www.duitang.com/album/?id=98243426&spm=2014.12553688.202.0}
# @File : ${duitang}.py
# @Software: ${PyCharm}

import requests  # 导入网页请求
import re  # 导入正则
import os  # 导入操作系统
import logging  # 导入日志
import xlwt  # 导入表格写入
import xlrd  # 导入表格读取
# import sys  # 导入系统
from xlutils.copy import copy  # 导入追加表格
from database import *

# 网页网址
url = 'https://www.duitang.com/album/?id=98243426&spm=2014.12553688.202.0'


def request_headers(logger):
    """
    网页请求时进行伪装，成功时打印日志“网页请求伪装已完成！”，失败时打印日志"网页请求伪装错误！"
    :param logger: 打印日志的对象，通过“.”可打印不同级别的日志
    :return: 伪装信息的字典
    """
    logger.debug("开始执行网页请求伪装！")
    # 伪装
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)/'
                          ' Chrome/78.0.3904.108 Safari/537.36'
        }
        logger.debug("网页请求伪装已完成！")
        return headers
    except:
        logger.error("网页请求伪装错误！")
    pass


def get_url(url, headers, logger):
    """
    进行网页请求，成功时返回网页信息并打印日志"网页请求已成功！"，失败时打印日志"网页请求错误！"，
    :param url: 网页网址
    :param headers: 伪装信息的字典
    :param logger: 打印日志的对象，通过“.”可打印不同级别的日志
    :return: 网页信息
    """
    logger.debug("开始请求网页！")
    try:
        # 请求网页
        response = requests.get(url=url, headers=headers)
        # print(response.text)
        # print(response.request.headers)
        response.encoding = 'UTF-8'
        html = response.text
        # print(html)
        logger.info("网页请求已成功！")
        return html
    except:
        logger.error("网页请求错误！")
    logger.debug("网页请求执行完毕！")
    pass


def re_url(html, logger):
    """
    利用正则解析网页，成功时返回文件名和图片网址并打印日志"网页解析已完成！"，失败时打印日志"解析网页错误！"
    :param html: 网页信息
    :param logger: 打印日志的对象，通过“.”可打印不同级别的日志
    :return: 保存图片的文件夹名，图片网址
    """
    logger.debug("开始解析网页！")
    try:
        # 解析保存图片的文件夹名
        # dir_name = re.findall('<h1 class="post-title h3">(.*?)</h1>', html)[-1]
        dir_name = re.findall('<meta name="keywords" content="(.*?)" />', html)
        # print(dir_name)
        dir_name = str(dir_name[0])
        # 解析网址
        # print(dir_name)
        img_urls = re.findall('<img data-rootid=".*?" alt=".*?" data-iid="" src="(.*?)" height=".*?"/>', html)
        # print(img_urls)
        logger.info("网页解析已完成！")
        return dir_name, img_urls
    except:
        logger.error("解析网页错误！")
    logger.debug("网页解析执行完毕！")
    pass


def mk_dir(dir_name, logger):
    """
    成功时如果文件夹不存在则创建文件夹并打印日志"文件夹“" + dir_name +"”创建成功！"，文件夹存在则打印日志
    "文件夹“" + dir_name + "”已存在！"；失败时打印日志"文件夹创建错误！"
    :param dir_name: 保存图片的文件夹名
    :param logger: 打印日志的对象，通过“.”可打印不同级别的日志
    :return: 无返回值
    """
    logger.debug("开始创建文件夹！")
    try:
        # 创建文件夹
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
            logger.info("文件夹“" + dir_name +"”创建成功！")
            pass
        else:
            logger.info("文件夹“" + dir_name + "”已存在！")
            pass
    except:
        logger.error("文件夹创建错误！")
    logger.debug("创建文件夹执行完毕！")
    pass


def get_photo(img_urls, dir_name, headers, save_path, logger):
    """
    保存图片和图片信息，成功时打印日志"保存图片成功！"，失败时打印日志"保存图片错误！"
    :param img_urls: 图片网址
    :param dir_name: 保存图片的文件夹名
    :param headers: 网页请求伪装信息
    :param save_path: 保存图片信息的文件路径
    :param logger: 打印日志的对象，通过“.”可打印不同级别的日志
    :return: 无返回值
    """
    logger.debug("开始保存图片！")
    try:
        # 图片信息列表
        img_info = []
        # 写入表格的行
        row = 3
        # 图片个数
        img_num = len(img_urls)
        img_count = 0
        # 保存图片
        for img_url in img_urls:
            img_count += 1
            # 写入表格的列
            column = 0
            # 图片名字
            file_name = img_url.split('/')[-1]
            file_name_part = file_name.split('.')[-1]
            # 文件名修正
            if file_name_part == 'webp':
                file_name_part = 'jpeg'
                file_name = ''.join(file_name.split('.')[0:-1]) + '.' + file_name_part
                pass

            # print(img_url)
            logger.info(img_url)
            # 请求网页
            response = requests.get(img_url, headers=headers)
            # 存储图片信息
            save_data(row, column, dir_name, file_name, img_url, img_num, img_count, save_path, logger)

            # 缓存图片信息
            img_info.append([dir_name, file_name, img_url])
            logger.info("缓存的图片信息列表：%s" % [dir_name, file_name, img_url])
            # 文件写入
            # with open(dir_name + '/' + file_name, 'wb') as file:
            #     file.write(response.content)
            #     # 下载提示
            #     logger.info('%s已下载' % file_name)
            # pass
            # with open('E:/pyproject/Django/appcao/static/appcao/image' + '/' + 'image'+ str(img_count)+'.jpg', 'wb') as file:
            with open(dir_name + '/' + 'image' + str(img_count) + '.jpg', 'wb') as file:
                file.write(response.content)
                # 下载提示
                logger.info('%s已下载' % file_name)
            pass
            row += 1
            logger.debug("保存图片成功！")
        logger.info("缓存的所有图片信息列表：%s" % img_info)
        return img_info
    except:
        logger.error("保存图片错误！")
    logger.debug("保存图片执行完毕！")
    pass


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


def save_data_init(save_path, logger):
    """
    创建保存图片信息的文件，成功时如果文件不存在则创建文件并打印日志"文件“" + save_path +"”创建成功！"，文件存在则打印日志
    "文件“" + save_path + "”已存在！"；失败时打印日志"保存图片信息的文件创建错误！"
    :param save_path: 保存图片信息的文件路径
    :param logger: 打印日志的对象，通过“.”可打印不同级别的日志
    :return: 无返回值
    """
    logger.debug("开始创建保存图片信息的文件！")
    try:
        if not os.path.exists(save_path):
            # 创建一个工作簿对象
            book = xlwt.Workbook(encoding="utf-8", style_compression=0)
            # 创建一个表格
            sheet = book.add_sheet('photo_info', cell_overwrite_ok=True)

            # 格式
            # 居中
            style = xlwt.XFStyle()
            al = xlwt.Alignment()
            al.horz = 0x02
            al.vert = 0x01
            style.alignment = al
            # 填充颜色
            pattern = xlwt.Pattern()
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN
            pattern.pattern_fore_colour = 0X1F
            style.pattern = pattern
            # 框线
            borders = xlwt.Borders()
            borders.left = xlwt.Borders.THIN
            borders.right = xlwt.Borders.THIN
            borders.top = xlwt.Borders.THIN
            borders.bottom = xlwt.Borders.THIN
            borders.left_colour = 0x40
            borders.right_colour = 0x40
            borders.top_colour = 0x40
            borders.bottom_colour = 0x40
            style.borders = borders

            # 字体
            font = xlwt.Font()
            font.name = '黑体'
            font.height = 20 * 11
            font.bold = False
            style.font = font

            # 写入合并单元格
            sheet.write_merge(0, 0, 0, 15, '保存图片的信息', style)
            sheet.write_merge(1, 1, 0, 15, '共计：', style)
            sheet.write_merge(2, 2, 0, 1, '存储位置', style)
            sheet.write_merge(2, 2, 2, 6, '文件名', style)
            sheet.write_merge(2, 2, 7, 15, '源链接', style)
            # 保存文件
            book.save(save_path)
            logger.info("文件“" + save_path + "”创建成功！")
            pass
        else:
            logger.info("文件“" + save_path + "”已存在！")
            pass
    except:
        logger.error("保存图片信息的文件创建错误！")
    logger.debug("创建保存图片信息的文件执行完毕！")
    pass


def save_data(row, column, dir_name, file_name, img_url, img_num, img_count, save_path, logger):
    """
    保存图片信息，成功时打印日志"追加写入数据成功！"，失败时打印日志"追加写入数据失败！"
    :param row: 信息写入表格的行
    :param column: 信息写入表格的列
    :param dir_name: 保存图片的文件夹名
    :param file_name: 图片名字
    :param img_url: 图片网址
    :param save_path: 保存图片信息的文件路径
    :param logger: 打印日志的对象，通过“.”可打印不同级别的日志
    :return: 无返回值
    """
    logger.debug("开始保存图片信息！")
    try:
        book = xlrd.open_workbook(save_path, formatting_info=True)
        # 将xlrd对象拷贝转化为xlwt对象
        new_book = copy(book)
        # 获取转化后工作簿中的第一个表格
        new_sheet = new_book.get_sheet(0)
        # 格式
        # 居中
        style = xlwt.XFStyle()
        al = xlwt.Alignment()
        al.horz = 0x02
        al.vert = 0x01
        style.alignment = al
        # 框线
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        borders.left_colour = 0x40
        borders.right_colour = 0x40
        borders.top_colour = 0x40
        borders.bottom_colour = 0x40
        style.borders = borders
        # 追加写入数据
        new_sheet.write_merge(row, row, column, column + 1, dir_name, style)
        new_sheet.write_merge(row, row, column + 2, column + 6, file_name, style)
        new_sheet.write_merge(row, row, column + 7, column + 15,  img_url, style)
        # 追加图片总数
        if img_count == img_num:
            # 字体
            font = xlwt.Font()
            font.name = '黑体'
            font.height = 20 * 11
            font.bold = False
            style.font = font
            new_sheet.write_merge(1, 1, 0, 15, '共计：' + str(img_num), style)
            pass
        # 保存文件
        new_book.save(save_path)
        logger.info("追加写入数据成功！")
    except:
        logger.error("追加写入数据失败！")
        pass
    logger.debug("保存图片信息执行完毕！")
    pass


if __name__ == "__main__":
    # 保存图片信息的文件路径
    save_path = 'duitang.xls'
    # 日志配置
    logger = get_logger()
    # 网页请求伪装
    headers = request_headers(logger)
    # 网页请求
    html = get_url(url, headers, logger)
    # 网页解析
    dir_name, img_urls = re_url(html, logger)
    # 创建保存图片的文件夹
    mk_dir(dir_name, logger)
    # 创建保存图片信息的文件
    save_data_init(save_path, logger)
    # 保存图片和图片信息
    img_info = get_photo(img_urls, dir_name, headers, save_path, logger)
    # 表格操作数据库连接
    var_connection = fun_connect_method(logger)
    # 创建数据库中的表格
    fun_create_method(var_connection, logger)
    # 将缓存的图片信息插入到数据库中的表格
    for img_info_element in img_info:
        fun_insert_method(var_connection, img_info_element, logger)
    pass
    # 从数据库中的表格中查询第X张图片信息
    fun_search_method(var_connection, 1, logger)
    # 表格操作数据库连接关闭
    fun_connect_close_method(var_connection, logger)
    pass







