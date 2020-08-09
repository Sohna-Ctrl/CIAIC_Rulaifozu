
#-*- encoding:utf-8 -*-
# @Time : ${08} ${08}
# @Author : 朱冰
# @Site : ${Xi‘an}
# @File : ${What to by}.py
# @Software: ${PRODUCT_NAME
#面向函数编程

import re, requests, xlwt,lxml
from lxml import etree
import logging
import xlrd
from xlutils.copy import copy


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"    # 日志格式化输出
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"                        # 日期格式
fp = logging.FileHandler('zhu-debug-log.txt', encoding='utf-8')
fs = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp, fs])    # 调用


try:
    def fun_crawler(website):

            while True:  # 一直循环，直到访问站点成功
                try:
                    url1 = website
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
                    }
                    response_1 = requests.get(url1, headers=headers, timeout=10)# 通过捕获然后等待网络情况的变化，以此来保护程序的不间断运行
                    break
                    # 以下except都是用来捕获当requests请求出现异常时，
                except requests.exceptions.ConnectionError:
                    print('ConnectionError -- please wait 3 seconds')
                    time.sleep(3)
                except requests.exceptions.ChunkedEncodingError:
                    print('ChunkedEncodingError -- please wait 3 seconds')
                    time.sleep(3)
                except:
                    print('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
                    time.sleep(3)
            response_1.encoding = 'utf-8'
            # print(response_1.text)
            return response_1.text
# 函数出现错误时显示输出
except Exception as e:
    logging.error('执行函数fun_crawler', exc_info=True)

#获得requests得到网页参数；解析网页获取商品名称，价格；将名称与价格作为返回值作为输出参数
try:
    def fun_web_analyse(webcontent):

        response_1 = webcontent# 获取网页list
        res_xpath = etree.HTML(response_1)#获得xpath，开始解析网页
        var_html_namesource_text = res_xpath.xpath('//div[@class="p_productCN"]//a[@target="_blank"]/text()') # 获取商品名字
        var_html_price_text = res_xpath.xpath('//div [@class="p_discount commonFontPrice"]/text()') #获取商品价格
        return var_html_namesource_text,var_html_price_text# 返回价格,名称
        # print(var_html_namesource_text)
        # print(var_html_price_text)
except Exception as e:
    logging.error('fun_web_analyse', exc_info=True)
    # logging.error('fun_web_analyse')


def main():
    # 使用循环爬取多个网页的内容
    var_webnum = 4
    list_01 = var_webnum * [0]
    list_webenum = var_webnum * [0]
    list_web_content=var_webnum * [0]
    list_web_price=[]
    list_web_name=[]
    #创建工作簿
    # workbook_01 = xlwt.Workbook()
    # #创建sheet
    # worbook_open_1 = xlrd.open_workbook('.//text.xls') # 打开xls文件
    # table = worbook_open_1.sheets()[0] # 打开第一张表
    # # sheet_01 = workbook_01.add_sheet(u'sheet1',cell_overwrite_ok=True)
    
    # 加载已存在的xls#，将已存在的excel拷贝进新的excel#，获取sheet
    workbook_test_old = xlrd.open_workbook('.//text.xls',formatting_info=True)
    workbook_test_new = copy(workbook_test_old)
    worksheet_01 = workbook_test_new.get_sheet(0)
    
    #大循环：向多个wensite请求，并获得网页内容，并将其作为的解析网页的输入
    for i in range(len(list_01)):
        list_webenum[i] = 'https://www.sephora.cn/hot/?k=%E7%95%85%E9%94%80%E6%A6%9C%E5%8D%95&hasInventory=0&sortField=1&sortMode=desc&currentPage=' + str(i+1)+'&filters='
        website=list_webenum[i]# 调用爬取网页的函数前将参数赋值
        list_web_content[i] =fun_crawler(website)# 调用爬取网页的函数,调用之后变量list_web_content中以列表的形式保存多个网页
        webcontent=list_web_content[i]# 准备调用网页解析函数,在调用网页解析函数之前将list中每个元素(代表每个网页的内容)保存
        f_web_analys = fun_web_analyse(webcontent)#将解析出的结果保存
        sublist_web_name=f_web_analys[0]#得到变量
        sublist_web_price=f_web_analys[1]
    
        #在excel中写入产品的名称与价格
        #设置excel的写入格式，包括单元格颜色，框线，底色
        # 设置单元格颜色
        style = xlwt.XFStyle()  # 格式信息
        pattern = xlwt.Pattern()  # Create the Pattern
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
        pattern.pattern_fore_colour = 31  # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
        style = xlwt.XFStyle()  # Create the Pattern
        style.pattern = pattern  # Add Pattern to Style
        # 给单元格加框线
        border = xlwt.Borders()
        border.left = xlwt.Borders.THIN  # 左
        border.top = xlwt.Borders.THIN  # 上
        border.right = xlwt.Borders.THIN  # 右
        border.bottom = xlwt.Borders.THIN  # 下
        border.left_colour = 0x40  # 设置框线颜色，0x40是黑色，颜色真的巨多，都晕了
        border.right_colour = 0x40
        border.top_colour = 0x40
        border.bottom_colour = 0x40
        style.borders = border
        # 单元格居中
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平方向
        alignment.vert = xlwt.Alignment.VERT_CENTER  # 竖直方向
        style.alignment = alignment
    
    
        # 小循环1-解析名称循环：解析大循环传来的网页信息，获得价格并在在excel中遍历单元格写入产品名称
        for j in range(len(sublist_web_name)):#以产品名称的个数为依据进行循环
            # sublist_web_name[j].replace(' ', '')
            worksheet_01.write(len(sublist_web_name) * i + j+1, 0, sublist_web_name[j],style)
            workbook_test_new.save('.\\text.xls')
    
        #小循环2-解析价格循环：解析大循环传来的网页信息，在excel中写入产品的价格 :分为三步，
        # 第一步为解析网页获得价格将产品的价格进行规范，
        # 第二步带~的价格与前一list的价格合并，
        # 第三步为将价格写入excel
        # 现在开始时第一步
        var_normhtml_price_text = []
        for j in range(len(sublist_web_price)):#与产品名称类似
            result = '~' in sublist_web_price[j]
            if result == False:
                var_normhtml_price_text.append(sublist_web_price[j])
                # a = var_normhtml_price_text
            else:
                var_normhtml_price_text.append(sublist_web_price[j - 1] + sublist_web_price[j])
                var_normprice = var_normhtml_price_text
                del var_normprice[len(var_normprice) - 2]#在新列表中删除重复元素
        # 现在开始是第二步
        for j in range(len(var_normprice)):
            # sublist_web_price[j].replace(' ', '')
            print(var_normprice[j])
            # print(j)
            worksheet_01.write(len(var_normprice) * i + j + 1, 1, var_normprice[j],style)
            workbook_test_new.save('.\\text.xls')
main()
# python调用vba
#使用xpath分析网页,将得到的每个网页中提取想要的消息,最终输出成两个list,
# 一个list中存商品的价格信息,另外一个list中保存商品的名称
#并将最终的list保存到excel文件中
# #将商品按品种分类"精华","套装","面膜","沐浴","分类",预计使用dict中的key
# def fun_show():
#
#     pass

