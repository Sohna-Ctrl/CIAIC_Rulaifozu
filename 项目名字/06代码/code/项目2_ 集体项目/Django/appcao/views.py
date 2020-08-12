from django.shortcuts import render

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

    if var_user_name == 'cjgong' and var_user_password == '123456':
        print('用户登录成功！')
        return render(request, 'appcao/success.html')
    else:
        print('用户登录失败！')
        return render(request, 'appcao/login.html')


