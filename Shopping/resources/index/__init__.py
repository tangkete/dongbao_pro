# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Api
from comment.utils.output import output_json

# 1\创建蓝图 2\到shopping app中注册蓝图使用
index_bp = Blueprint('index', __name__, url_prefix='/index')
# 创建一个商品分类的Api， 参数是蓝图
index_api = Api(index_bp)

# 自定义返回格式
index_api.representation('application/json')(output_json)

# 加载资源模块
from Shopping.resources.index.index_resource import *
index_api.add_resource(Shopping_Category, '/category', endpoint='category')
index_api.add_resource(IndexCategory, '/indexCategory', endpoint='indexCategory')
index_api.add_resource(Shopping_HomeNewProduct, '/home_new_product', endpoint='home_new_product')
index_api.add_resource(Shopping_HomeRecommendProduct, '/home_recommend_product', endpoint='home_recommend_product')
index_api.add_resource(Shopping_RecommendSubject, '/recommend_subject', endpoint='recommend_subject')
