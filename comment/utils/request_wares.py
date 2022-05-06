# -*- coding: utf-8 -*-
"""
    定义请求钩子：
    在请求进来之前得到request携带的token，并且验证token
    注意：用户没有登录前是没有token的
"""
from flask import g,request,current_app
from comment.utils.tokens_jwt import verify_tokens
def jwt_request_authorization():
    """
    自定义请求钩子函数，把验证通过的token，得到的用户id保存到全局变量中
    :return:
    """
    g.user_id = None # 定义一个变量user_id
    try:
        token = request.headers.get('token') # 从请求头得到token
        # current_app.logger.info('token:{}'.format(token))
    except Exception as e:
        current_app.logger.info('请求头中没有token:{}'.format(e))
        return
    result = verify_tokens(token)
    # 如果验证成功，那么字典中一定有用户id
    if 'id' in result:
        g.user_id = result['id']
