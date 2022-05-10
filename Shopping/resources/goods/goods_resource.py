# -*- coding: utf-8 -*-
import json
from flask_restful import Resource, reqparse, request
from comment.models.goods import Specification, SpecificationOption, SkuStock, ProductFullReduction
from comment.models.index import Product, Category
from comment.utils.data2dict import datalist2dict, data2dict
from comment.utils.shopping_redis import redis_client


class Goods_GoodsList(Resource):
    """
    商品列表
    """

    def post(self):
        rq = reqparse.RequestParser()
        rq.add_argument('page', required=True, type=int)
        rq.add_argument('num', required=True, type=int)
        req = rq.parse_args()
        self.page_num = req.page  # 页码
        self.page_size = req.num  # 数量
        self.relCategory1Id = request.form.get('relCategory1Id')
        self.relCategory2Id = request.form.get('relCategory2Id')
        self.relCategory3Id = request.form.get('relCategory3Id')
        self.search_word = request.form.get('productName')
        if self.relCategory1Id:
            cache_data = redis_client.get("goods_goodslist_relCategory1Id_{}_{}_{}".format(self.relCategory1Id, self.page_num, self.page_size))
            if cache_data:
                return json.loads(cache_data)
        if self.relCategory2Id:
            cache_data = redis_client.get("goods_goodslist_relCategory2Id_{}_{}_{}".format(self.relCategory2Id, self.page_num, self.page_size))
            if cache_data:
                return json.loads(cache_data)
        if self.relCategory3Id:
            cache_data = redis_client.get("goods_goodslist_relCategory3Id_{}_{}_{}".format(self.relCategory3Id, self.page_num, self.page_size))
            if cache_data:
                return json.loads(cache_data)

        res = self.select_search()
        if res:
            data = {}
            data['has_next'] = res.has_next  # 是否还有下一页
            data['has_prev'] = res.has_prev  # 是否还有上一页
            data['next_num'] = res.next_num  # 下一页的页码
            data['page'] = res.page  # 当前页的页码
            data['per_page'] = res.per_page  # 每页显示的数量
            data['pages'] = res.pages  # 匹配的元素在当前配置一共有多少页
            data['total'] = res.total  # 匹配的元素总数
            data['content'] = datalist2dict(res.items)
            redis_client.setex("goods_goodslist_{}_{}_{}".format(self.redis_key, self.page_num, self.page_size), 3600, json.dumps(data))
            return data
        else:
            return {'msg':'none'}

    def select_search(self):
        self.res_filter = None
        if self.relCategory1Id:
            self.res_filter = Product.query.filter(Product.rel_category1_id == self.relCategory1Id)
            self.redis_key = "relCategory1Id_{}".format(self.relCategory1Id)
        if self.relCategory2Id:
            self.res_filter = Product.query.filter(Product.rel_category2_id == self.relCategory2Id)
            self.redis_key = "relCategory2Id_{}".format(self.relCategory2Id)
        if self.relCategory3Id:
            self.res_filter = Product.query.filter(Product.rel_category3_id == self.relCategory3Id)
            self.redis_key = "relCategory3Id_{}".format(self.relCategory3Id)
        if self.search_word:
            self.res_filter = Product.query.filter(Product.product_name.like("%"+self.search_word+"%"))
            self.redis_key = "search_word_{}".format(self.search_word)
        if self.res_filter:
            # res 是一个paginate 对象， 需要用res.items 遍历对象返回的内容
            res = self.res_filter.with_entities(
                Product.id, Product.product_name, Product.rel_category3_id,Product.default_pic, Product.price)\
                .paginate(page=self.page_num, per_page=self.page_size,error_out=True)
            if res:
                return res
            else:
                return {'message':'none'}
        else:
            return None


class Goods_GoodsSpecification(Resource):
    """
    商品规格
    """

    def post(self):
        self.relCategory1Id = request.form.get('relCategory1Id')
        self.relCategory2Id = request.form.get('relCategory2Id')
        self.relCategory3Id = request.form.get('relCategory3Id')
        self.search_word = request.form.get('productName')
        res = self.get_spec_list()
        return res or {'msg': 'none', 'code': 200}

    def get_spec_list(self):
        self.res = None
        # 先查询relCategory1Id分类下的所有商品数据
        if not any([self.relCategory1Id, self.relCategory2Id, self.relCategory3Id, self.search_word]):
            return {'msg':'请检查参数:relCategory1Id 、 relCategory2Id、 relCategory3Id ，不能全部为空'}, 400
        if self.relCategory1Id:
            self.res = Product.query.filter(Product.rel_category1_id == self.relCategory1Id)
        if self.relCategory2Id:
            self.res = Product.query.filter(Product.rel_category2_id == self.relCategory2Id)
        if self.relCategory3Id:
            self.res = Product.query.filter(Product.rel_category3_id == self.relCategory3Id)
        if self.search_word:
            self.res = Product.query.filter(Product.product_name.like("%"+self.search_word+"%"))

        res_with_entities = self.res.with_entities(Product.spec_options).first()
        # print('res_with_entities:', res_with_entities)
        if not res_with_entities:
            return None

        # 拿到对应分类商品或所搜商品的规格列表。
        product_spec = res_with_entities.spec_options.split(',')
        spec_list = []

        for spec in product_spec:
            # 用规格id查询规格的名称和id （颜色 内存 屏幕大小等）
            spec_name = Specification.query.filter(Specification.id == int(spec)).with_entities\
                (Specification.name, Specification.id).first()
            # 用规格id查询规格的具体分类 （ 颜色下面的，红色，蓝色等）
            spec_info = SpecificationOption.query.filter(SpecificationOption.rel_spec_id == int(spec)).with_entities\
                (SpecificationOption.name, SpecificationOption.id, SpecificationOption.enabled,
                 SpecificationOption.rel_spec_id).all()
            optionList = datalist2dict(spec_info)
            spec_list.append({
                'specId': spec_name.id,
                'specName': spec_name.name,
                'optionList': optionList
            })

        return spec_list


class Goods_GoodsDetail(Resource):
    """
        商品详情
    """

    def get(self):
        rq = reqparse.RequestParser()
        rq.add_argument('good_id', type=int)
        req = rq.parse_args()
        self.pruduct_id = req.good_id

        # 获取查询的产品
        product_res = Product.query.filter(Product.id == self.pruduct_id).first()

        if not product_res:
            return {'msg': 'none'}

        goods_detail_data = data2dict(product_res)
        pro_sku_data = self.get_sku_data(self.pruduct_id)
        goods_detail_data['skuList'] = [pro_sku_data, ]
        spec_list = []

        # 用规格id查询规格的名称和id （颜色 内存 屏幕大小等）
        spec_all = Specification.query.filter(
            Specification.rel_category_id == product_res.rel_category3_id).with_entities \
            (Specification.id, Specification.name, Specification.rel_category_id, Specification.rel_spec_type_id).all()
        for spec in spec_all:
            temp_data = data2dict(spec)

            spec_info = SpecificationOption.query.filter(SpecificationOption.rel_spec_id == spec.id).with_entities \
                (SpecificationOption.name, SpecificationOption.id, SpecificationOption.enabled,
                 SpecificationOption.rel_spec_id).all()
            option_list = datalist2dict(spec_info)
            temp_data['optionDTOS'] = option_list
            spec_list.append(temp_data)

        goods_detail_data['specList'] = spec_list
        return goods_detail_data

    def get_sku_data(self, pruduct_id):
        # 获取查询的产品的sku
        pro_sku_res = SkuStock.query.filter(SkuStock.rel_product_id == pruduct_id).first()
        pro_sku_data = data2dict(pro_sku_res)
        # 获取sku下面的规格列表
        specTypeList = json.loads(pro_sku_data['spec'])
        pro_sku_data['specTypeList'] = specTypeList
        return pro_sku_data

class Goods_GoodSkuDetail(Resource):
    """
    获取产品sku
    """
    def post(self):
        rq = reqparse.RequestParser()
        rq.add_argument('productId', type=int)
        rq.add_argument('optionIds', type=str)
        req = rq.parse_args()
        self.productId = req.productId
        self.optionIds = req.optionIds
        res_sku = SkuStock.query.filter(SkuStock.rel_product_id == self.productId,
                                        SkuStock.option_ids == self.optionIds).first()
        if res_sku:
            sku_data = data2dict(res_sku)
            specTypeList = json.loads(sku_data['spec'])
            sku_data['specTypeList'] = specTypeList
            return sku_data
        else:
            return {'msg': 'none'}

    @staticmethod
    def get_sku_by_id(sku_id):
        res_sku = SkuStock.query.filter(SkuStock.id == sku_id).with_entities\
            (SkuStock.id, SkuStock.price).first()
        if res_sku:
            return data2dict(res_sku)
        else:
            return {'msg': 'none'}

class Goods_Recommend(Resource):
    """
    商品推荐 (购物车)
    """

    def post(self):
        rq = reqparse.RequestParser()
        rq.add_argument('relProductId', type=int)
        req = rq.parse_args()
        rel_productId = req.relProductId

        res = Product.query.filter(Product.rel_category3_id == rel_productId).order_by \
            (-Product.sales_num).limit(8).all()

        if res:
            res_data = datalist2dict(res)
            return res_data
        else:
            return {'msg': 'none'}

class Goods_MerchantHotsales(Resource):
    """
    商家热卖
    """

    def get(self):
        rq = reqparse.RequestParser()
        rq.add_argument('merchant_id', type=int)
        req = rq.parse_args()
        self.merchant_id = req.merchant_id

        res = Product.query.filter(Product.rel_tenant_id == self.merchant_id).order_by \
            (-Product.sales_num).limit(5).all()

        if res:
            res_data = datalist2dict(res)
            return res_data
        else:
            return {'msg': 'none'}



class Goods_GoodsFullReduction(Resource):
    """
        商品满减
    """
    def get(self):
        rq = reqparse.RequestParser()
        rq.add_argument('good_id', type=int)
        req = rq.parse_args()
        self.product_id = req.good_id
        return self.get_fullReduction(self.product_id)

    def get_fullReduction(self, product_id):
        res = ProductFullReduction.query.filter(ProductFullReduction.product_id == product_id).with_entities(
            ProductFullReduction.id, ProductFullReduction.product_id, ProductFullReduction.full_price,
            ProductFullReduction.reduce_price, ProductFullReduction.start_time, ProductFullReduction.end_time).all()
        data_list = []

        if res:
            for item in res:
                res_data = data2dict(item)
                data_list.append(res_data)
            return data_list
        else:
            return {'msg': 'none'}


class Goods_CartSkuDetail(Resource):
    """
    购物车 优惠sku
    """
    def post(self):
        rq = reqparse.RequestParser()
        rq.add_argument('sku_list', required=True)
        req = rq.parse_args()
        sku_list_json = req.sku_list
        sku_list = json.loads(sku_list_json)   # 购物车的sku列表

        data_list = []

        for item in sku_list:
            sku_id = item['skuId']
            num = int(item['num'])
            product_id = SkuStock.query.filter(SkuStock.id == sku_id).first().rel_product_id
            # sku对应商品的满减
            res = ProductFullReduction.query.filter(ProductFullReduction.product_id == product_id).with_entities\
                (ProductFullReduction.id,ProductFullReduction.reduce_price, ProductFullReduction.full_price).first()
            if res:
                item_full_reduction = data2dict(res)
                # sku信息，sku价格 sku id
                item_sku_info = Goods_GoodSkuDetail.get_sku_by_id(sku_id)
                reduce_price = item_full_reduction['reduce_price']
                if item_sku_info['price'] * num >= item_full_reduction['full_price']:
                    discountPrice = item_sku_info['price'] * num - reduce_price
                else:
                    discountPrice = item_sku_info['price'] * num
                    reduce_price = 0


                data = {
                    'discountPrice': discountPrice,
                    'originPrice': item_sku_info['price'],
                    'reducePrice': reduce_price,
                    'reductionId': item_full_reduction['id'],
                    'skuId': item_sku_info['id']
                }
                data_list.append(data)
        return data_list


