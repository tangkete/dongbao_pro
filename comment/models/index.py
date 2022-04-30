# -*- coding: utf-8 -*-

from comment.models import db
from sqlalchemy import text
# 商品分类
class Category(db.Model):
    __tablename__ = 't_category'
    __table_args__ = {'comment': '商品分类'}

    id = db.Column(db.BigInteger, primary_key=True)
    level = db.Column(db.SmallInteger, server_default=text("1"), comment='层级')
    parent_id = db.Column(db.BigInteger, server_default=text("0"), comment='ID')
    name = db.Column(db.String(255), comment="中文")
    en = db.Column(db.String(255), comment='英语')
    sort = db.Column(db.Integer, comment='排序，暂未使用')
    catid = db.Column(db.Integer, comment='类目id，关联pid使用')
    catid_use = db.Column(db.SmallInteger, default=0, comment='是否使用catid查询')
    query_t = db.Column(db.String(255), comment='淘宝查询')
    query_t_use = db.Column(db.SmallInteger, default=1, comment='是否使用query')
    weight = db.Column(db.Float, comment='类目单元配重')
    status = db.Column(db.SmallInteger, default=1, comment='状态')
    gmt_create = db.Column(db.BigInteger, nullable=False, default=0, comment='创建时间')
    gmt_modified = db.Column(db.BigInteger, nullable=False, default=0, comment='更新时间')
    create_uid = db.Column(db.String(64), nullable=False, default=0, comment='创建人uid')
    create_uname = db.Column(db.String(64), nullable=False, default=0, comment='创建人昵称')
    modified_uid = db.Column(db.String(64), nullable=False, default=0, comment='更新人uid')
    modified_uname = db.Column(db.String(64), nullable=False, default=0, comment='更新人昵称')
    enabled = db.Column(db.SmallInteger, nullable=False, default=0, comment='是否删除:0-未删除;1-删除')
    merchant_id = db.Column(db.String(32), comment='商户ID')
