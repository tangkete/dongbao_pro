# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Api
from comment.utils.output import output_json

# 1\创建蓝图 2\创建蓝图中的资源Api 3\到shopping app中注册蓝图使用

test_bp = Blueprint('testapi', __name__, url_prefix='/testapi')
test_api = Api(test_bp)

test_api.representation('application/json')(output_json)


from Shopping.resources.test.test_resource import *
test_api.add_resource(TestCase, '/test', endpoint='test')
