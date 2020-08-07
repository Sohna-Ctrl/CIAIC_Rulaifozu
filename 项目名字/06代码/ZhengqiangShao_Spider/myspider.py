#-*- encoding:utf-8 -*-
# @Time : 2020/8/7 15:09
# @Author : Zhengqiang Shao
# @Site : 
# @File : myspider.py
# @Software: PyCharm

from bs4 import BeautifulSoup          # 网页解析，获取数据
import re           # 正则表达式，进行文字匹配
import urllib.request,urllib.error      # 指定URL，获取网页数据
import xlwt         # 进行excel操作
import sqlite3      # 进行SQLITE操作


def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1.爬取网页
    datalist = getData(baseurl)
    save_path = ".\\豆瓣电影Top250.xls"
    # 2.获取数据
    # 3.保存数据
    saveData(datalist,save_path)
    pass

# 影片详情链接的规则
findLink = re.compile(r'<a href="(.*?)">')#r是忽视所有的特殊符号#   #创建正则表达式对象。表示规则，
#2，影片图片
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)#
# 影片的名字
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 影片的评分
findRating  = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
#找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
#找到影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)


# 1.爬取网页
def getData(baseurl):
    datalist = []
    for index in range(0,10):
        url = baseurl + str(index * 25)
        html = askULR(url)

        # 逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):
            # print(item)测试查看电影item
            data = []  # 保存一部电影的全部信息
            item = str(item)
            # print(item)
            # break
            link = re.findall(findLink, item)[0]  # re库用来查找指定的字符串，用指定的字符串。
            data.append(link)

            ImgSrc = re.findall(findImgSrc, item)[0]  # 查找符合要求的字符串，形成列表
            data.append(ImgSrc)

            titles = re.findall(findTitle, item)  # 找到的名字可能有两个
            if (len(titles) == 2):
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/", "")  # 去掉无关的符号
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')  # 留空，外国名字留空
            rating = re.findall(findRating, item)[0]  # 添加评分
            data.append(rating)

            judgeNum = re.findall(findJudge, item)[0]  # 添加人数
            data.append(judgeNum)

            inq = re.findall(findInq, item)  #
            if len(inq) != 0:
                inq = inq[0].replace("。", "")  # 去掉句号
                data.append(inq)
            else:
                data.append(" ")

            bd = re.findall(findBd, item)[0]  #
            bd = re.sub('<br>(\s+)?>(\s+)?', "", bd)  # 去掉<br>
            bd = re.sub('/', " ", bd)  # 去掉/
            data.append(bd.strip())  # 去掉空格

            datalist.append(data)  # 把处理好的一部电影放入datalist

    # print(datalist)
    return datalist

# 得到指定的一个URL的网页内容
def askULR(url):
    head = {
        #模拟头部信息，向豆瓣服务器发送消息
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }
    #封装头部信息
    requst = urllib.request.Request(url=url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(requst)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html


# 保存数据
def saveData(datalist,save_path):
    print("save...")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet("豆瓣电影Top250",cell_overwrite_ok=True)
    col = ["电影详细链接","图片链接","影片中文名","影片英文名","评分","评价数","概述","详细信息"]
    for index in range(0,8):
        sheet.write(0,index,col[index])
    for row_Index in range(0,250):
        print("第%d条"%(row_Index+1))
        data = datalist[row_Index]
        for col_Index in range(0,8):
            sheet.write(row_Index+1,col_Index,data[col_Index])
    book.save("save_path")
    pass





if __name__ == "__main__":           #当程序执行时
    main()