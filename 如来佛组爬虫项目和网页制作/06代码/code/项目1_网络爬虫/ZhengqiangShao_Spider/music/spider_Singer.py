#-*- encoding:utf-8 -*-
# @Time : 2020/8/8 0:16
# @Author : Zhengqiang Shao from CIAIC
# @Site : 
# @File : spider_Singer.py.py
# @Software: PyCharm

##-------此次爬虫任务:爬取豆瓣音乐中最受欢迎的音乐人Top20，保存歌手的姓名，流派，成员，唱片公司以及喜欢人数和歌手主页------##

# i引入第三方库
from bs4 import BeautifulSoup           # 网页解析，获取数据
from xlutils.copy import copy           # 对文件读写
import re                               # 正则表达式，进行文字匹配
import urllib.request,urllib.error      # 指定URL，获取网页数据
import xlwt,xlrd                        # 进行excel操作
import logging                          # 为程序添加日志


def main():
    logger = get_logger()            # 打印日志的初始配置
    baseUrl = "https://music.douban.com/artists/top20"      # ii爬取的网站
    # iii1.爬取网站
    dataList = getData(baseUrl, logger)
    # 3.保存数据
    savePath = "豆瓣音乐最受欢迎音乐人Top20.xls"
    saveData(dataList, savePath, logger)
    pass

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
def askULR(url,logger):
    logger.info('开始获取豆瓣音乐"最受欢迎音乐人 Top20 "的网页内容')
    head = {
        # 模拟头部信息，向豆瓣服务器发送消息
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }
    # 封装头部信息
    requst = urllib.request.Request(url=url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(requst)
        html = response.read().decode("utf-8")
        logger.info("获取网页内容成功！")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            logger.error(e.code)
        if hasattr(e,"reason"):
            logger.error(e.reason)
    return html


# 1.爬取每个歌手信息网页
def getData(baseUrl,logger):
    logger.info("开始爬取网页内容")
    dataList = []
    # iii获取网页的html代码
    html = askULR(baseUrl,logger)
    # 解析音乐人的个人信息
    logger.info("开始进行网页内容解析")
    Singers = BeautifulSoup(html,"html.parser")
    # iiii对每位音乐人进行信息解析
    for singer in Singers.find_all('div',class_="site_bar"):
        singer = str(singer)
        data = []

        # 找到音乐人名字
        Image = re.findall(findName,singer)[0]
        data.append(Image)

        # 找到音乐人的个人信息链接
        Info = re.findall(findInfo,singer)[0]
        Info = Info.split('"')[0]
        data.append(Info)

        # 流派
        School = re.findall(findschool,singer)[0]
        School = School.split("\n")[0]
        data.append(School)

        # 成员
        Member = re.findall(findmember,singer)[0]
        Member = Member.replace('\n', "")  # 去掉\n
        Member = Member.split()
        for index in Member:
            tem = ""
            tem += index
        Member = tem
        data.append(Member)

        # 唱片公司
        Company = re.findall(findComp,singer)
        if len(Company) != 0:
            Company = Company[0]
            Company = Company.split("\n")[0]
            data.append(Company)
        else:
            data.append(" ")

        # 喜欢人数
        Number = re.findall(findNume,singer)
        Number = str(Number)
        Number = Number.split(" ")[-1]
        Number = Number.split("'")[0]
        data.append(Number)
        dataList.append(data)
    logger.info("网页内容解析结束")
    return dataList


# 3.iiii保存数据
def saveData(dataList,savePath,logger):
    logger.info("开始进行 Top20 歌手的指定信息保存")
    # 设置字体大小，字体位置，字体背景
    style_1 = xlwt.easyxf('font: bold on,height 300;''align: horiz center;''borders: left thin, right thin, top thin, bottom thin;''pattern: pattern solid, fore_colour sea_green')
    style_2 = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;''pattern: pattern solid, fore_colour gray25')
    style_3 = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;''pattern: pattern solid, fore_colour ice_blue')

    book = xlrd.open_workbook("豆瓣音乐最受欢迎音乐人Top20.xls",formatting_info=True)
    excel = copy(wb=book)                                               #完成xlrd对象向xlwt对象转换
    excel_table = excel.get_sheet(0)                                    #获得要操作的sheet
    col = ["音乐人","音乐人个人链接","流派","团队成员","唱片公司","喜欢人数"]
    excel_table.write_merge(0,0,0,5,"豆瓣音乐最受欢迎音乐人Top20",style_1)            #对excel合并单元格
    for colIndex in range(0,6):                                         #写入标题
        excel_table.write(1,colIndex,col[colIndex],style_2)
    for rowIndex in range(0,20):
        # print("%d个音乐人被写入"%(rowIndex+1))
        data = dataList[rowIndex]
        for colIndex in range(0,6):
            excel_table.write(rowIndex+2,colIndex,data[colIndex],style_3)
    excel.save(savePath)
    logger.info("excel数据保存成功！")
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
    main()
pass

