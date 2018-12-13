from django.shortcuts import render, redirect

from user.forms import RegisterForm

from django.contrib.auth.hashers import make_password,check_password

from .models import User

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
    if req.method == "POST":
        nickname = req.POST.get('nickname').strip()
        password = req.POST.get('password').strip()

        #检查用户是否存在
        try:
            user = User.objects.get(nickname=nickname)
        except User.DoesNotExist:
            return render(req,'login.html',{'error': '用户不存在'})

        #检查密码是否正确
        if check_password(password,user.password):
            req.session['uid'] = user.id
            req.session['nickname'] = user.nickname
            req.session['avatar'] = user.icon.url
            return redirect('/user/info/')

        else:
            return render(req,'login.html',{'error':'密码错误'})
    else:
        return render(req,'login.html',{})

#退出
def logout(req):
    req.session.flush()
    return redirect('/')

#用户信息
def user_info(req):
    uid = req.session.get('uid')
    user = User.objects.get(pk=uid)
    return render(req,'user_info.html',{'user':user})