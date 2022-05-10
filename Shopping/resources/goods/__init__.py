# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Api
from comment.utils.output import output_json

# 1\创建蓝图 2\创建蓝图中的资源Api 3\到shopping app中注册蓝图使用
goods_bp = Blueprint('goods', __name__, url_prefix='/goods')
goods_api = Api(goods_bp)

# 自定义api的返回格式
goods_api.representation('application/json')(output_json)

# 加载资源模块
from Shopping.resources.goods.goods_resource import *

goods_api.add_resource(Goods_GoodsList, '/goods_list', endpoint='goods_list')
goods_api.add_resource(Goods_GoodsSpecification, '/goods_specification', endpoint='goods_specification')
goods_api.add_resource(Goods_GoodsDetail, '/good_detail', endpoint='goods_detail')
goods_api.add_resource(Goods_GoodsFullReduction, '/good_fullReduction', endpoint='good_fullReduction')
goods_api.add_resource(Goods_MerchantHotsales, '/merchant_hotsales', endpoint='merchant_hotsales')
goods_api.add_resource(Goods_GoodSkuDetail, '/good_sku_detail', endpoint='good_sku_detail')
goods_api.add_resource(Goods_CartSkuDetail, '/goods_cart_sku_detail', endpoint='goods_cart_sku_detail')
goods_api.add_resource(Goods_Recommend, '/goods_cart_recommend', endpoint='goods_cart_recommend')
