from django.core.cache import cache
from requests import post

from common import rds
from post.models import Post


def page_cache(view_func):
    #页面缓存
    def wrapper(request):

        #定义缓存 key
        session_id = request.session.session_key
        url = request.get_full_path()
        key = 'PageCache-%s-%s' % (session_id,url)

        #从缓存获取Response
        response = cache.get(key)
        print('get from cache:',response)
        if response is None:
            # 执行View函数，并将response加入缓存
            response = view_func(request)
            cache.set(key,response)
            print('get from view:',response)
        return response
    return wrapper

def get_top_n(num):
    '''
    获取阅读计数前n的文章数据
     Args:
         num: 排行前 N
     Return:
        rank_data: [
            [Post(9),100],
            [Post(5),91],
            [Post(7),79],
        ]
    '''

    # origin_data = [
    #     (b'1',37.0),
    #     (b'517',16.8),
    #     (b'510',12.0),
    # ]

    origin_data = rds.zrevrange('ReadCounter',0,num - 1,withscores=True)

    # cleaned_data = [
    #     [1,37],
    #     [517,16],
    #     [510,12],
    # ]

    cleaned_data = [[int(post_id),int(count)] for post_id,count in origin_data]

    #方法一：
    # for item in cleaned_data:
    #     post_id = item[0]
    #     post = Post.objects.get(pk=post_id)
    #     item[0] = post

    #方法二：批量获取，减少对数据库的操作
    # post_id_list = [post_id for post_id, _ in cleaned_data]  #提取所有的post_id
    # posts = Post.objects.filter(id__in = post_id_list)
    # posts = sorted(posts,key=lambda post:post_id_list.index(post.id)) #按照post_id_list 顺序进行排序
    #
    # for item,post in zip(cleaned_data,posts): #zip 起迭代器的作用
    #     item[0] = post

    #方法三：
    post_id_list = [post_id for post_id, _ in cleaned_data]  # 提取所有的POST ID
    posts = Post.objects.in_bulk(post_id_list)

    for item in cleaned_data:
        post_id = item[0]
        item[0] = posts[post_id]

    return cleaned_data