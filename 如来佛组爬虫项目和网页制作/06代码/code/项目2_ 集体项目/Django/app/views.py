from django.shortcuts import render, redirect


# Create your views here.


# 显示登陆页面
def fun_method01(request):
    return render(request, 'app/login.html')


# 处理登录功能
def fun_method02(request):
    # 获取页面输入内容
    print(request)
    var_dict = request.GET
    var_user_name = var_dict.get('user_name')
    var_user_password = var_dict.get('user_password')

    if var_user_name == 'cao' and var_user_password == 'cao':
        print('用户登录成功！')
        return redirect('/app/index/')
    elif var_user_name == 'shao' and var_user_password == 'shao':
        print('用户登录成功！')
        return redirect('/app/index/')
    elif var_user_name == 'jia' and var_user_password == 'jia':
        print('用户登录成功！')
        return redirect('/app/index/')
    elif var_user_name == 'tang' and var_user_password == 'tang':
        print('用户登录成功！')
        return redirect('/app/index/')
    elif var_user_name == 'zhu' and var_user_password == 'zhu':
        print('用户登录成功！')
        return redirect('/app/index/')
    else:
        print('用户登录失败！')
        return render(request, 'app/login.html')


# 显示主页
def fun_method03(request):
    return render(request, 'app/index.html')

