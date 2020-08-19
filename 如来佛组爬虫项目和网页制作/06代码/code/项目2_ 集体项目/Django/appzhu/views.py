from django.shortcuts import render
from  django.http import  HttpResponse
from appzhu import zhubingpachong
# Create your views here.

#  显示页面
def fun_mehthod01(request):
	return render(request,'appzhu/index.html')

#  启动网络爬虫进行数据爬取
def fun_mehthod02(request):
	#  调用爬虫方法
	#  返回列表
	var_list_01=zhubingpachong.getlistmain()
	# 把数据保存到字典里
	var_dict_01=dict(padata=var_list_01)
	return render(request,'appzhu/table_BTF.html',context=var_dict_01)


def fun_mehthod03(request):
	return render(request,'appzhu/chart.html')


def fun_mehthod04(request):
	return render(request,'appzhu/chart2.html')
