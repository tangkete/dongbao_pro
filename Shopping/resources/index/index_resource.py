# -*- coding: utf-8 -*-
from flask import current_app
from flask_restful import Resource, request, reqparse
from comment.models.index import *  # 导入资源类
from comment.utils.data2dict import datalist2dict
from comment.utils.shopping_redis import redis_client
import json

# 商品分类资源类
class Shopping_Category(Resource):

    def get(self):
        # 从redis 读取数据， 如果有，则返回，如果没有则将数据写入redis
        date_cache = redis_client.get("index_category")
        if date_cache:
            return json.loads(date_cache)
        else:
            # 添加RequestParser请求
            rq = reqparse.RequestParser()
            rq.add_argument('parent_id', type=int, required=True) #添加请求参数 parent_id ，数据类型int， 必填为True
            req = rq.parse_args() # 获取请求参数
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
                redis_client.setex('index_category', 3600*24, json.dumps(data))
                return data
            else:
                current_app.logger.info("data is none!")
                return {'message':'data is none!'}

    @staticmethod
    def getDate(parent_id):
        # 从数据库查询字段
        # with_entities 查询指定的字段
        res = Category.query.with_entities(Category.id, Category.parent_id, Category.name)\
        .filter(Category.parent_id==parent_id).order_by(Category.sort.asc()).all()
        if res:
            return datalist2dict(res)
        else:
            return 'none'
