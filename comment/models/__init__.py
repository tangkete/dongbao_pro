# -*- coding: utf-8 -*-
# 模型类
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from .user import User
from .index import Category
from .goods import SkuStock
