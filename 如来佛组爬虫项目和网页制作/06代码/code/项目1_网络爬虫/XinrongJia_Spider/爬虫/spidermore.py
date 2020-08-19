#-*- encoding:utf-8 -*-
# @Time : 2020/8/9 17:58
# @Author : 贾欣融
# @Site : 
# @File : spidermore.py
# @Software: PyCharm
#代码信息

import bs4
from bs4 import BeautifulSoup
import re
import urllib
import urllib.request
import xlwt
import logging

def main():
    baseurl = "https://y.music.163.com/m/discover/toplist?id=3778678"  #网易云音乐热歌榜

    # 1.爬取网页
    list_inf = getData(baseurl)
    savepath = "网易云音乐热歌榜top200.xls"

    # 3.保存数据
    saveData(list_inf, savepath)

findalbum_inf = re.compile(r'"album":{"id":(.*?),"name":"(.*?)","picUrl":"(.*?)"')
findartist_inf = re.compile(r'"artists":\[{"id":(.*?),"name":"(.*?)",')

#爬取网页
def getData(baseurl):
    datalist = []
    # artist_item=[]
    # 网易云热歌榜只有一页，所以不使用for循环


    html = askURL(baseurl)

    # print(type(html))
    # 2.逐一解析数据
    soup = BeautifulSoup(html, "html.parser")
    item = soup.find('ul', class_="f-hide").find_all('a')

    artist_item = soup.find('textarea').string

    artist_item = str(artist_item)
    album_inf = re.findall(findalbum_inf, artist_item)
    artist_inf = re.findall(findartist_inf, artist_item)
    #'https://music.163.com/#/album?id=' + album_inf[1][0]

    logger.info("网页爬取成功")

    # print(album_inf)
    # print(len(album_inf))
    # print(artist_inf)
    # print(len(artist_inf))


    # for song_num in range(0,200):
    #     song_inf=artist_item[song_num]
    #     print(song_inf)
    #https://music.163.com/#/album?id=92510920

    data_name = []
    data_url = []

    # 查找符合要求的字符串，形成列表
    for a in item:
        music_url = 'https://music.163.com'+a['href']
        music_name = a.text
        # print(music_name,music_url)
        # item = str(item)
        # print(item)
        # link = re.findall(findLink, item)  #正则
        data_name.append(music_name)
        data_url.append(music_url)
        # print(type(link))
        # datalist.append(data)
    # datalist.append(data_name)
    # datalist.append(data_url)
    # print(datalist)

    list_inf=[data_name, data_url, album_inf, artist_inf]
    print(list_inf[0])

    return list_inf

#得到指定的一个URL的网页内容
def askURL(url):

    logger.info("模拟浏览器")
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
      }
#用户代理告诉服务器模拟浏览器
    logger.info("开始爬取网页")
    request = urllib.request.Request(url, headers=head)
#携带头部信息访问url
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html

#保存数据
def saveData(list_inf,savepath):


    style_1 = xlwt.easyxf(
        'font: bold on,height 500;''align: horiz center;''borders: left thin, right thin, top thin, bottom thin;''pattern: pattern solid, fore_colour coral')
    style_2 = xlwt.easyxf(
        'font: bold on,height 230;''borders: left thin, right thin, top thin, bottom thin;''pattern: pattern solid, fore_colour light_blue')
    style_3 = xlwt.easyxf(
        'borders: left thin, right thin, top thin, bottom thin;''pattern: pattern solid, fore_colour gold')
    style_4 = xlwt.easyxf(
        'borders: left thin, right thin, top thin, bottom thin;''pattern: pattern solid, fore_colour ice_blue')
    style_5 = xlwt.easyxf(
        'borders: left thin, right thin, top thin, bottom thin;''pattern: pattern solid, fore_colour pale_blue')
    
    data_name = list_inf[0]
    data_url = list_inf[1]
    album_inf = list_inf[2]
    artist_inf = list_inf[3]

    logger.info("开始保存数据")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('网易云音乐热歌榜', cell_overwrite_ok=True)

    sheet.write_merge(0, 0, 0, 7, "网易云音乐热歌榜信息", style_1)  # 对excel合并单元格

    col = ("歌曲排名", "歌名", "歌曲链接", "歌手名字", "歌手主页链接", "专辑名字", "专辑链接", "歌曲封面图片链接")
    for i in range(0, 8):
        sheet.write(1, i, col[i], style_2)
    for i in range(0, 200):
        logger.info("第%d条" %(i+2))
        # data = datalist[i]
        sheet.write(i + 2, 0, i + 1, style_3)
        # for j in range(1, 3):
        #     sheet.write(i+1, j, data[j-1])
        song_name = data_name[i]
        song_url = data_url[i]
        sheet.write(i + 2, 1, song_name , style_4)
        sheet.write(i + 2, 2, song_url , style_5)

        artist_url='https://music.163.com/#/artist?id=' + artist_inf[i][0]
        artist_name= artist_inf[i][1]
        sheet.write(i + 2, 3, artist_name , style_4)
        sheet.write(i + 2, 4, artist_url , style_5)

        album_url =  'https://music.163.com/#/album?id=' + album_inf[i][0]
        album_name= album_inf[i][1]
        pic_url = album_inf[i][2]
        sheet.write(i + 2, 5, album_name , style_4)
        sheet.write(i + 2, 6, album_url , style_5)
        sheet.write(i + 2, 7, pic_url  , style_4)

    book.save(savepath)   # 保存
    logger.info("保存数据完成！")

#设置日志
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

if __name__ == "__main__":
# 调用函数
    logger = get_logger()
    main( )
    logger.info("爬取完毕!")