

# Create your views here.
from django.shortcuts import render, redirect
# 引入第三方库
from bs4 import BeautifulSoup  # 网页解析，获取数据
from xlutils.copy import copy  # 对文件读写
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 指定URL，获取网页数据
import xlwt, xlrd  # 进行excel操作
import logging  # 为程序添加日志


def fun_method01(request):
 return render(request, 'appshao/login.html')


def fun_method04(request):
 return render(request, 'appshao/navigation.html')


# 显示网页
def fun_method03(request):

    # 把数据保存到字典里

    def main():
     logger = get_logger()  # 打印日志的初始配置
     baseUrl = "https://music.douban.com/artists/top20"
     # 1.爬取网站
     dataList = getData(baseUrl, logger)
     return dataList

    # # 歌手名字
    findName = re.compile(r'<a.*href=".*?">(.*?)</a>')
    # 歌手信息链接
    findInfo = re.compile(r'.*href="(.*?)">.*</a>')
    # 流派
    findschool = re.compile(r'<div>.*流派:(.*?)/.*</div>', re.S)
    # 成员
    findmember = re.compile(r'<div>.*成员:(.*?)/.*</div>', re.S)
    # 唱片公司
    findComp = re.compile(r'<div>.*唱片公司:(.*?)/.*</div>', re.S)
    # 喜欢人数
    findNume = re.compile(r'/.*\n(.*?)人喜欢.*</div>', re.S)

    # 得到指定的一个URL的网页内容
    def askULR(url, logger):
     logger.info('开始获取豆瓣音乐"最受欢迎音乐人 Top20 "的网页内容')
     head = {
      # 模拟头部信息，向豆瓣服务器发送消息
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
     }
     # 封装头部信息
     requst = urllib.request.Request(url=url, headers=head)
     html = ""
     try:
      response = urllib.request.urlopen(requst)
      html = response.read().decode("utf-8")
      logger.info("获取网页内容成功！")
     except urllib.error.URLError as e:
      if hasattr(e, "code"):
       logger.error(e.code)
      if hasattr(e, "reason"):
       logger.error(e.reason)

     return html

    # 1.爬取每个歌手信息网页
    def getData(baseUrl, logger):
     logger.info("开始爬取网页内容")
     dataList = []
     html = askULR(baseUrl, logger)
     # 解析歌手的名字和图片链接
     logger.info("开始进行网页内容解析")
     Singers = BeautifulSoup(html, "html.parser")

     for singer in Singers.find_all('div', class_="site_bar"):
      singer = str(singer)
      data = []

      # 找到音乐人名字
      Image = re.findall(findName, singer)[0]
      data.append(Image)

      # 找到音乐人的个人信息链接
      Info = re.findall(findInfo, singer)[0]
      Info = Info.split('"')[0]
      data.append(Info)

      # 流派
      School = re.findall(findschool, singer)[0]
      School = School.split("\n")[0]
      data.append(School)

      # 成员
      Member = re.findall(findmember, singer)[0]
      Member = Member.replace('\n', "")  # 去掉\n
      Member = Member.split()
      for index in Member:
       tem = ""
       tem += index
      Member = tem
      data.append(Member)

      # 唱片公司
      Company = re.findall(findComp, singer)
      if len(Company) != 0:
       Company = Company[0]
       Company = Company.split("\n")[0]
       data.append(Company)
      else:
       data.append(" ")

      # 喜欢人数
      Number = re.findall(findNume, singer)
      Number = str(Number)
      Number = Number.split(" ")[-1]
      Number = Number.split("'")[0]
      data.append(Number)
      dataList.append(data)
     logger.info("网页内容解析结束")
     return dataList

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
    # 爬虫
    var_list_01 = main()
    var_dict_01 = dict(padata=var_list_01)
    return render(request, 'appshao/navigation.html', context=var_dict_01)


def fun_method02(request):
 # 获取页面输入内容
 print(request)
 var_dict = request.GET
 var_user_name = var_dict.get('user_name')
 var_user_password = var_dict.get('user_password')
 if var_user_name == 'shao' and var_user_password == 'shao':
  print('用户登录成功！')
  return redirect('/appshao/index/')
 else:
  print('用户登录失败！')
  return render(request, 'appshao/login.html')
