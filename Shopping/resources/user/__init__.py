# -*- coding: utf-8 -*-

# 用户模块下的蓝图：包括用户模块的所有资源
from flask import Blueprint
from flask_restful import Api
from comment.utils.output import output_json
from comment.utils.request_wares import jwt_request_authorization

# 创建蓝图url_prefix 一级路径/user
user_bp = Blueprint('users', __name__, url_prefix='/user')
user_api = Api(user_bp) # 创建蓝图中的资源api

# 在当前用户模块中添加请求钩子，通过蓝图加
# user_bp.before_request(jwt_request_authorization)

# 使用自定义json格式，可以代替装representation饰器的写法,注意representation饰器的写法没有s
user_api.representation('application/json')(output_json)


# 加载当前资源模块
from Shopping.resources.user.user_resource import Shopping_user, SendMessage, AuthorizationCodeResource, RegisterUserResource,\
    UserLoginResource,IsExistPhoneResource
user_api.add_resource(Shopping_user, '/user', endpoint='user') # 请求路径为{ip}/user/user
user_api.add_resource(SendMessage, '/sms', endpoint='sms') # 请求路径为{ip}/user/sms
user_api.add_resource(AuthorizationCodeResource, '/authorization', endpoint='authorization')
user_api.add_resource(RegisterUserResource, '/register', endpoint='register')
user_api.add_resource(UserLoginResource, '/login', endpoint='login') # /user/login
user_api.add_resource(IsExistPhoneResource, '/isExist', endpoint='isExist')
