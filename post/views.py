from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

#创建帖子
def create_post(req):
    return render(req,"create_post.html",{})



#修改帖子
def edit_post(req):
    return render(req,"edit_post.html",{})

#阅读帖子
def read_post(req):
    return render(req,"read_post.html",{})

#删除帖子
def delete_post(req):
    return render(req,"delete_post.html",{})

#查看列表
def post_list(req):
    return render(req,"post_list.html",{})

#搜索
def search(req):
    return render(req,"search.html",{})
