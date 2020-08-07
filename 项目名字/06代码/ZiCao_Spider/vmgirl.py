# -*- encoding:utf-8 -*-
# @Time : ${20/08/07} ${18:00}
# @Author : 曹梓
# @Site : ${https://www.vmgirls.com/14101.html}
# @File : ${vmgirl}.py
# @Software: ${PyCharm}

import requests  # 导入网页请求
import re  # 导入正则
import os  # 导入操作系统
# url = 'https://www.vmgirls.com/14236.html'
url = 'https://www.vmgirls.com/14101.html'
# 伪装
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

# 请求网页
response = requests.get(url=url, headers=headers)
# print(response.text)
# print(response.request.headers)
response.encoding = 'UTF-8'  # 编码格式
html = response.text
# print(html)

# 解析网页
dir_name = re.findall('<h1 class="post-title h3">(.*?)</h1>', html)[-1]  # 解析文件名
# 创建文件夹
if not os.path.exists(dir_name):
    os.mkdir(dir_name)
    pass
urls = re.findall('<a href="(.*?)" alt=".*?" title=".*?">', html)  # 解析网址

# 网址修正
k = 0  # 列表索引
for url in urls:
    url = 'https://www.vmgirls.com/' + url  # 修正网址
    urls[k] = url  # 修改列表
    k += 1
    pass
print(urls)

# 保存图片
for url in urls:
    file_name = url.split('/')[-1]  # 图片名字
    response = requests.get(url, headers=headers)  # 请求网页
    # 文件写入
    with open(dir_name+'/' + file_name, 'wb') as file:
        file.write(response.content)
        print('%s已下载' % file_name)  # 下载提示
    pass



