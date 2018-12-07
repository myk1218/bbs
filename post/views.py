from math import ceil

from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Post
# Create your views here.

#创建帖子
def create_post(req):
    if req.method == "POST":
        title = req.POST.get("title")
        content = req.POST.get("content")
        post = Post.objects.create(title = title,content = content)
        return redirect('/post/read/?post_id=%d'% post.id)
    else:
        return render(req,"create_post.html")

#修改帖子
def edit_post(req):
    if req.method == "POST":
        post_id = int(req.POST.get('post_id'))
        post = Post.objects.get(pk=post_id)
        post.title = req.POST.get("title")
        post.content = req.POST.get("content")
        post.save()
        return redirect('/post/read/?post_id=%d'% post.id)
    else:
        post_id = int(req.GET.get('post_id'))
        post = Post.objects.get(pk=post_id)
        return render(req,"edit_post.html",{'post':post})

#阅读帖子
def read_post(req):
    post_id = int(req.GET.get('post_id'))
    post = Post.objects.get(pk=post_id)
    return render(req,"read_post.html",{'post':post})

#删除帖子
def delete_post(req):
    post_id = int(req.GET.get('post_id'))
    Post.objects.get(pk=post_id).delete()
    return redirect('/')

#查看列表
def post_list(req):
    page = int(req.GET.get('page',1))  #当前页码
    total = Post.objects.count() #文章数量
    per_page = 10                #每页显示10篇
    pages = ceil(total/per_page) #页数

    start = (page - 1) * per_page #当前页开始索引
    end = start + per_page  #当前页结束索引
    posts = Post.objects.all()[start:end]

    return render(req,"post_list.html",{'posts':posts,'pages':range(pages)})

#搜索
def search(req):
    keyword = req.POST.get('keyword')
    posts = Post.objects.filter(title__contains=keyword)
    return render(req,"search.html",{'posts':posts})
