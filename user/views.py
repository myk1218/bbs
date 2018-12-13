from django.shortcuts import render, redirect

from user.forms import RegisterForm

from django.contrib.auth.hashers import make_password,check_password

# Create your views here.

#注册
def register(req):
    if req.method == 'POST':
        form = RegisterForm(req.POST,req.FILES)
        if form.is_valid():
            user = form.save(commit=False) #commit = False表示不提交
            user.password = make_password(user.password)
            user.save()
            return redirect('/user/login/')
        else:
            return render(req,'register.html',{'error':form.errors})
    else:
        return render(req,'register.html')

#登录
def login(req):
    return render(req,'login.html',{})

#退出
def logout(req):
    return redirect('/')

#用户信息
def user_info(req):
    return render(req,'user_info.html',{})