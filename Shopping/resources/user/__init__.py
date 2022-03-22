# -*- coding: utf-8 -*-

# 用户模块下的蓝图：包括用户模块的所有资源

from flask import Blueprint
from flask_restful import Api
from comment.utils.output import output_json

# 创建蓝图
user_bp = Blueprint('users', __name__, url_prefix='/user')
user_api = Api(user_bp) # 创建蓝图中的资源api




# 使用自定义json格式，可以代替装representation饰器的写法,注意representation饰器的写法没有s
user_api.representation('application/json')(output_json)



# 加载当前资源模块
from Shopping.resources.user.user_resource import Shopping_user
user_api.add_resource(Shopping_user, '/hello', endpoint='user')
