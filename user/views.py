from django.shortcuts import render, redirect

from django.conf import settings

from user.forms import RegisterForm

from django.contrib.auth.hashers import make_password,check_password

from user.helper import get_wb_access_token, wb_user_show
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
            return render(req,'login.html',{'error': '用户不存在','auth_url': settings.WB_AUTH_URL})

        #检查密码是否正确
        if check_password(password,user.password):
            req.session['uid'] = user.id
            req.session['nickname'] = user.nickname
            req.session['avatar'] = user.icon.url
            return redirect('/user/info/')

        else:
            return render(req,'login.html',{'error':'密码错误','auth_url': settings.WB_AUTH_URL})
    else:
        return render(req,'login.html',{'auth_url': settings.WB_AUTH_URL})

#退出
def logout(req):
    req.session.flush()
    return redirect('/')

#用户信息
def user_info(req):
    uid = req.session.get('uid')
    user = User.objects.get(pk=uid)
    return render(req,'user_info.html',{'user':user})

def weibo_callback(req):
    '微博回调接口'
    code = req.GET.get('code')

    #获取access_token
    access_token,wb_uid = get_wb_access_token(code)
    if access_token is None:
        return render(req,'login.html',{'error':'微博 Token 接口错误','auth_url':settings.WB_AUTH_URL})

    #获取微博的用户数据
    screen_name,avatar = wb_user_show(access_token, wb_uid)
    if screen_name is None:
        return render(req,'login.html',{'error':'微博 User 接口错误','auth_url':settings.WB_AUTH_URL})

    #利用微博的账号，在论坛内进行登录注册
    nickname = '%s_wb'% screen_name
    user,is_created = User.objects.get_or_create(nickname=nickname)
    user.plt_icon = avatar
    user.save()

    #记录用户状态
    req.session['uid'] = user.id
    req.session['nickname'] = user.nickname
    req.session['avatar'] = user.avatar

    return redirect('/user/info/')