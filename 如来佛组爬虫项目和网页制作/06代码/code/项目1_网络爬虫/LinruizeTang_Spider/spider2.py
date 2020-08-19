#-*- encoding:utf-8 -*-
# @Time : 2020/8/11 15:05
# @Author : 唐林瑞泽
# @Site : 
# @File : spider2.py
# @Software: PyCharm

#-*- encoding:utf-8 -*-
# @Time : 2020/8/10 23:16
# @Author : 唐林瑞泽
# @Site :
# @File : test7.py
# @Software: PyCharm


import re
import urllib
import xlwt
from bs4 import BeautifulSoup


def fun_main():
    # 保存地址列表
    dataall = []
    address = ['https://www.youtube.com/watch?v=GfO-3Oir-qM&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=1',
               'https://www.youtube.com/watch?v=cTQ3Ko9ZKg8&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=2',
               'https://www.youtube.com/watch?v=um2Q9aUecy0&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=3',
               'https://www.youtube.com/watch?v=r9PeYPHdpNo&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=4',
               'https://www.youtube.com/watch?v=XmtXC_n6X6Q&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=5',
               'https://www.youtube.com/watch?v=9FqwhW0B3tY&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=6',
               'https://www.youtube.com/watch?v=R2DU85qLfJQ&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=7',
               'https://www.youtube.com/watch?v=JkaxUblCGz0&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=8',
               'https://www.youtube.com/watch?v=aGGBGcjdjXA&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=9',
               'https://www.youtube.com/watch?v=krfcq5pF8u8&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=10',
               'https://www.youtube.com/watch?v=YCSo2hZRcXk&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=11',
               'https://www.youtube.com/watch?v=Lrm2pD0qofM&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=12',
               'https://www.youtube.com/watch?v=fQM6t1oSQkE&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=13',
               'https://www.youtube.com/watch?v=HRvGlB1-Ku8&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=14',
               'https://www.youtube.com/watch?v=Xb33zXpEgCc&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=15',
               'https://www.youtube.com/watch?v=C65iqOSCZOY&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=16',
               'https://www.youtube.com/watch?v=hP8dLUxBfsU&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=17',
               'https://www.youtube.com/watch?v=ZCFkWDdmXG8&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=18',
               'https://www.youtube.com/watch?v=NZGLHdcw2RM&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=19',
               'https://www.youtube.com/watch?v=W-9vb_-qzaQ&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=20',
               'https://www.youtube.com/watch?v=Mqrhn8khGLM&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=21',
               'https://www.youtube.com/watch?v=q_k8fVNzbGU&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=22',
               'https://www.youtube.com/watch?v=kaSvGVhtszo&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=23',
               'https://www.youtube.com/watch?v=jo4aAVjuh2o&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=24',
               'https://www.youtube.com/watch?v=rKeFCd1j5BE&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=25',
               'https://www.youtube.com/watch?v=vzJuhOn3Y58&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=26',
               'https://www.youtube.com/watch?v=LCfBYE97rFk&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=27',
               'https://www.youtube.com/watch?v=BDpqt-haLLM&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=28',
               'https://www.youtube.com/watch?v=5f7fHHEr_NA&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=29',
               'https://www.youtube.com/watch?v=YOv5jDFtvsI&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=30',
               'https://www.youtube.com/watch?v=1T3RHuPB_cg&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=31',
               'https://www.youtube.com/watch?v=BFtbXwnBRg8&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=32',
               'https://www.youtube.com/watch?v=KJCL9LR6rJI&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=33',
               'https://www.youtube.com/watch?v=p1otGt99Rec&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=34']
    for i in address:  # 调用获取页面信息的函数1次
        baseurl = i
        datalist = fun_get_data(baseurl)
        dataall.append(datalist)
    print(dataall)


    # 2.逐一解析数据(边爬取边解析)

# 3.保存数据
    savepath = ".\\youtube_NETFLIX纪录片.xls"
    # fun_save_data(savepath)
    # fun_ask_URL("https://www.youtube.com/watch?v=GfO-3Oir-qM&list=PLvahqwMqN4M0GRkZY8WkLZMb6Z-W7qbLA&index=1")
    # fun_save_data(datalist,savepath)
    fun_save_data(dataall, savepath)

# 查找纪录片的链接
findLink = re.compile(r'<link href="(.*?)" rel="shortlink"/>')  # 创建正则表达式对象，表示规则（字符串的模式）
# 查找纪录片的图片
findImgSrc = re.compile(r'<link href="(.*?)" itemprop="thumbnailUrl"/>')
#  纪录片的片名
findTitle = re.compile(r'<meta content=".*?" name="title"/')
# 纪录片描述
findDiscription = re.compile(r'<meta content=".*?" name="description"/')
# 纪录片关键词
findKeywords = re.compile(r'<meta content=".*?" name="keywords"/')

# 爬取网页
def fun_get_data(baseurl):

    datalist = []
    url = baseurl
    html = fun_ask_URL(url)  # 保存获取到的网页源码
    # 2.逐一解析数据(边爬取边解析)
    soup = BeautifulSoup(html, "html.parser")
    data = []
    # 查找符合要求的字符串，形成列表
    for item in soup.find_all('link'):
        # print(item)
        # 测试：查看纪录片item的全部信息
        #data = []  # 保存一部电影的所有信息
        item = str(item)
        link = re.findall(findLink, item)
        if link != []:  # 排除空列表
                url_video = link
                #print(url_video)
                #data.append(url_video)
                #datalist.append(url_video)
                datalist = datalist + url_video



    # 查找图片信息
    for item in soup.find_all('link'):  # 查找符合要求的字符串，形成列表
        # print(item)
        # #测试：查看纪录片item的全部信息
        #data = []
        item = str(item)
        link = re.findall(findImgSrc, item)
        if link != []:
            url_image = link
            # print(url_image)
            #data.append(url_image)
            #datalist.append(url_image)
            datalist = datalist + url_image



    # 查找片名
    for item in soup.find_all('meta'):  # 查找符合要求的字符串，形成列表
        # print(item)
        # #测试：查看纪录片item的全部信息
        #data = []
        item = str(item)
        link = re.findall(findTitle, item)
        if link != []:
            url_title = link
            # print(url_title)
            #data.append(url_title)
            #datalist.append(url_title)
            datalist = datalist + url_title



    # 查找描述
    for item in soup.find_all('meta'):  # 查找符合要求的字符串，形成列表
        # print(item)
        # #测试：查看纪录片item的全部信息
        #data = []
        item = str(item)
        link = re.findall(findDiscription, item)
        if link != []:
            url_description = link
            # print(url_description)
            #data.append(url_description)
            #datalist.append(url_description)
            datalist = datalist + url_description



    # 查找关键词
    for item in soup.find_all('meta'):  # 查找符合要求的字符串，形成列表
        # print(item)
        # #测试：查看纪录片item的全部信息
        #data = []
        item = str(item)
        link = re.findall(findKeywords, item)
        if link != []:
            url_keywords = link
            #print(url_keywords)
            #data.append(url_keywords)
            #print(data)
            #datalist.append(url_keywords)
            datalist = datalist + url_keywords
            #datalist.append(data)  # 将处理好的信息放入datalist

    #print(datalist)
    # print(data)
    return datalist







# 得到指定一个URL的网页内容
def fun_ask_URL(url):
    head = {         # 模拟浏览器头部信息，向youtube服务器发送信息
        "user-agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64)"
                      " AppleWebKit / 537.36(KHTML, like Ge"
                      "cko) Chrome / 79.0.3945.79 Safari / 537.36"
    }
    # 用户代理，表示告诉youtube我们是什么类型的机器，
    # 浏览器（本质上是告诉浏览器，我们可以接受什么水平的文件内容）
    request = urllib.request.Request(url, headers=head)
    html = ""

    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)

    return html


#3.保存数据
def fun_save_data(dataall,savepath):
    print("save....")
    workbook = xlwt.Workbook(encoding="utf-8",style_compression=0)  # 创建workbook对象
    worksheet = workbook.add_sheet('youtube_NETFLIX纪录片',cell_overwrite_ok= True)  # 创建工作表
    col = ("影片链接","封面图片链接","片名","描述","关键字") #列名称
    for i in range(0,5):
        worksheet.write(0,i,col[i])  #列名
    for i in range(0,34):
        print("第%d条"%i)
        data = dataall[i]
        for j in range(0,5):  #填写每一行信息
            worksheet.write(i+1,j,data[j])
    workbook.save('documentary.xls')


if __name__ == "__main__": # 当程序执行时调用函数
    fun_main()
    print("爬取完毕")