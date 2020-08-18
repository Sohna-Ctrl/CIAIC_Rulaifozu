from django.shortcuts import render, redirect
from appcao.duitang import *
# Create your views here.


# 显示登陆页面
def fun_method01(request):
    return render(request, 'appcao/login.html')


# 处理登录功能
def fun_method02(request):
    # 获取页面输入内容
    print(request)
    var_dict = request.GET
    var_user_name = var_dict.get('user_name')
    var_user_password = var_dict.get('user_password')

    if var_user_name == 'cao' and var_user_password == 'cao':
        print('用户登录成功！')
        return redirect('/appcao/personal/')
    else:
        print('用户登录失败！')
        return render(request, 'appcao/login.html')


# 显示个人主页
def fun_method03(request):
    return render(request, 'appcao/personal.html')


# 图片展示
def fun_method04(request):
    return render(request, 'appcao/photodisp.html')


# 图片信息展示
def fun_method05(request):
    # 调用爬虫方法
    # 返回列表
    img_info_list = main()
    # 列表元素修正
    var_num = 0
    for element in img_info_list:
        var_num = var_num + 1
        element.insert(0, str(var_num))
    # 把数据存入字典
    img_info_dict = dict(datapa=img_info_list)
    return render(request, 'appcao/phototable.html', context=img_info_dict)
