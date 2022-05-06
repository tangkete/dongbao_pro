# -*- coding: utf-8 -*-
from flask import current_app
from flask_restful import Resource, request, reqparse
from comment.models.index import *  # 导入资源类
from comment.utils.data2dict import datalist2dict
from comment.utils.shopping_redis import redis_client
import json

# 商品分类资源类
class IndexCategory(Resource):

    def get(self):
        # 添加RequestParser请求
        rq = reqparse.RequestParser()
        rq.add_argument('parent_id', type=int, required=True)  # 添加请求参数 parent_id ，数据类型int， 必填为True
        req = rq.parse_args()  # 获取请求参数
        # 从redis 读取数据， 如果有，则返回，如果没有则将数据写入redis
        date_cache = redis_client.get("index_category_id{}".format(req.parent_id))
        if date_cache:
            return json.loads(date_cache)  #字符串loads转为字典
        else:
            data = self.getDate(req.parent_id)
            if data and data != "none":
                for item in data: # 返回的一级分类数据添加二级分类返回
                    item.update({'list':''})
                    data_second = self.getDate(item['id'])
                    item['list'] = data_second
                    for titem in data_second: # 返回的二级分类下添加三级分类返回
                        titem.update({'list':''})
                        data_t = self.getDate(titem['id'])
                        titem['list'] = data_t
                # 将数据写入redis， 参数一key名， 参数二有效时长 ， 参数三 数据value，写入时需转为str
                redis_client.setex('index_category_id{}'.format(req.parent_id), 3600*24, json.dumps(data))
                return data
            else:
                current_app.logger.info("data is none!")
                return {'msg':'data is none!'}

    @staticmethod
    def getDate(parent_id):
        # 从数据库查询字段
        # with_entities 查询出指定的字段
        res = Category.query.with_entities(Category.id, Category.parent_id, Category.name)\
        .filter(Category.parent_id == parent_id).order_by(Category.sort.asc()).all()
        if res:
            return datalist2dict(res)
        else:
            return 'none'

class Shopping_Category(Resource):
    def get(self):
        cached_data = redis_client.get("index_category")
        if cached_data:
            return json.loads(cached_data)
        else:
            data = self.getData(0)
            if data:
                for item in data:
                    item.update({'list': ''})
                    data_second = self.getData(int(item['id']))
                    item['list'] = data_second
                    for item1 in data_second:
                        item1.update({'list': ''})
                        data_third = self.getData(int(item1['id']))
                        item1['list'] = data_third
                redis_client.setex("index_category", 3600*36, json.dumps(data))
                return data
            else:
                return {'message': 'none'}

    @staticmethod
    def getData(parent_id):
        # 从数据库查询字段
        # with_entities 查询出指定的字段
        res = Category.query.with_entities(Category.id, Category.parent_id, Category.name)\
        .filter(Category.parent_id == parent_id).order_by(Category.sort.asc()).all()
        if res:
            return datalist2dict(res)
        else:
            return 'none'


class Shopping_HomeNewProduct(Resource):
    def get(self):
        cache_data = redis_client.get("index_HomeNewProduct")
        if cache_data:
            return json.loads(cache_data)
        else:
            # 通过新品推荐商品的商品id 和商品表的商品id关联
            res = HomeNewProduct.query.join(Product, HomeNewProduct.product_id == Product.id)\
                .with_entities(Product.id, Product.default_pic, Product.product_name,
                               Product.rel_category3_id, Product.price).order_by(HomeNewProduct.sort.asc()).limit(10).all()
            if res:
                data = datalist2dict(res)
                redis_client.setex("index_HomeNewProduct", 3600*24, json.dumps(data))
                return data
            else:
                return {'msg':'None'}

# 人气热搜商品
class Shopping_HomeRecommendProduct(Resource):
    def get(self):
        cache_data = redis_client.get("index_HomeRecommendProduct")
        if cache_data:
            return json.loads(cache_data)
        else:
            res = HomeRecommendProduct.query.join(Product, HomeRecommendProduct.product_id == Product.id)\
                .with_entities(Product.id, Product.product_name, Product.price, Product.rel_category3_id, Product.default_pic)\
                .order_by(HomeRecommendProduct.sort.asc()).all()
            if res:
                data = datalist2dict(res)
                redis_client.setex("index_HomeRecommendProduct", 3600*24, json.dumps(data))
                return data
            else:
                return {'msg': 'data is none'}
# 首页专题资源类
class Shopping_RecommendSubject(Resource):
    def get(self):
        cache_data = redis_client.get("index_recommend_subject")
        if cache_data:
            return json.loads(cache_data)
        else:
            res = CmsSubject.query.filter(CmsSubject.show_status == 1).all()
            if res:
                data = datalist2dict(res)
                for i in range(len(data)):
                    res_product = CmsSubjectProductRelation.query.join(Product, CmsSubjectProductRelation.product_id == Product.id)\
                                    .filter(CmsSubjectProductRelation.subject_id == data[i]['id'])\
                                    .with_entities(Product.product_name, Product.id, Product.rel_category3_id,
                                       Product.default_pic, Product.price).limit(10).all()
                    if res_product:
                        data[i]['productList'] = datalist2dict(res_product)
                    else:
                        data[i]['productList'] = ''
                redis_client.setex("index_recommend_subject", 3600*24, json.dumps(data))
                return data
            else:
                return {'msg': 'data is none'}
