#-*- encoding:utf-8 -*-
# @Time : ${08} ${08}
# @Author : 朱冰
# @Site : ${Xi‘an}
# @File : ${What to by}.py
# @Software: ${PRODUCT_NAME

import re, requests, xlwt,lxml
from lxml import etree


# 所爬取网页地址/什么值得买
url1 = 'https://www.smzdm.com/fenlei/gehuhuazhuang/p2'
#
#此处写一个循环，将上述p2改动从而获取更多的资源
#
# #添加请求头
# #
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
response_1 = requests.get(url1, headers=headers)
response_1.encoding = 'utf-8'
# print(response_1.text)
res_xpath=etree.HTML(response_1.text)

# #获取商品名称
var_html_namesource_text=res_xpath.xpath('//h5//a//text()')
#获取商品价格
var_html_price_text=res_xpath.xpath('//div[@class="side-price"]//text()')
print(var_html_namesource_text)
print(var_html_price_text)



#
#存入excel excel输出产品按种类排序，按价格展示






