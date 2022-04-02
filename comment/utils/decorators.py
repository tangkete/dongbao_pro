# -*- coding: utf-8 -*-
"""
    装饰器，
    某些请求如果登录后才让进行下一步操作，验证token是否存在
    如果没有登录则跳转到登录页
"""

from flask import g

def login_required(func):
    def wrapper(*args, **kwargs):
        if g.user_id is not None: # user_id非空，已经登录过
            return func(*args, **kwargs)
        else:
            return {'msg': 'Invalid token'}, 400
    return wrapper
