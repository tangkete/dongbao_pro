# -*- coding: utf-8 -*-
from flask_restful import Resource
from comment.models.user import User


# 定义资源类
class Shopping_user(Resource):
    def get(self):
        # 可能需要用到User模型类
        # 返回json对象
        return {'hello':'测试'}

    def post(self):
        pass

