from math import ceil

from django.core.cache import cache

from django.shortcuts import render, redirect

from .models import Post

from common import rds
# Create your views here.

from post.helper import page_cache

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

        #更新帖子缓存
        key = 'Post-%s'% post_id
        cache.set(key,post)
        print('缓存更新')
        return redirect('/post/read/?post_id=%d'% post.id)
    else:
        post_id = int(req.GET.get('post_id'))
        post = Post.objects.get(pk=post_id)
        return render(req,"edit_post.html",{'post':post})

#阅读帖子
def read_post(req):
    post_id = int(req.GET.get('post_id'))

    key = 'Post-%s'%post_id
    post = cache.get(key)
    print('从缓存里获取：',post)
    
    if post is None:
        #从数据库取出数据，并且添加到缓存里
        post = Post.objects.get(pk=post_id)
        cache.set(key,post)
        print('从数据库里获取',post)

    # 增加阅读计数
    rds.zincrby('ReadCounter',post_id)
    return render(req,"read_post.html",{'post':post})

#删除帖子
def delete_post(req):
    #删除对象
    post_id = int(req.GET.get('post_id'))
    Post.objects.get(pk=post_id).delete()
    rds.zrem('ReadCounter',post_id) #同时删除排行数据
    return redirect('/')

#查看列表
@page_cache
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

def top10(req):
    rank_data = [
        [Post(9),100],
        [Post(5),91],
        [Post(7),79]
    ]
    return render(req,'top10.html',{'rank_data':rank_data})
