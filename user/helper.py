from django.conf import settings
import requests


def get_wb_access_token(code):

    #获取微博的Access Token

    #构造参数
    args = settings.WB_ACCESS_TOKEN_ARGS.copy()
    args['code'] = code

    #发送请求
    response = requests.post(settings.WB_ACCESS_TOKEN_API,data=args)

    #提取数据
    data = response.json()

    if 'access_token' in data:
        access_token = data['access_token']
        uid = data['uid']
        return access_token,uid
    else:
        return None,None

def wb_user_show(access_token,wb_uid):

    #根据微博用户id获取用户信息
    #构造参数
    args = settings.WB_USER_SHOW_ARGS
    args['access_token'] = access_token
    args['uid'] = wb_uid

    #发送请求
    response = requests.get(settings.WB_USER_SHOW_API,params=args)
    data = response.json()
    if 'screen_name' in data:
        screen_name = data['screen_name']
        avatar = data['avatar_hd']
        return screen_name,avatar
    else:
        return None,None
