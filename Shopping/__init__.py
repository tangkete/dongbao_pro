# -*- coding: utf-8 -*-
from flask import Flask
from settings import map_config


# 创建app对象
def create_app(config_type):
    app = Flask(__name__)
    # 加载项目的配置
    app.config.from_object(map_config.get(config_type))

    # 初始化限流器
    from comment.utils.limiter import limiter as lmt
    lmt.init_app(app)

    # 加载日志处理工具
    from comment.utils.logging_ import logger
    logger(app)

    # 初始化SQLAlchemy
    from comment.models import db
    db.init_app(app)

    # 初始化reids数据库链接
    from comment.utils.shopping_redis import redis_client
    redis_client.init_app(app)

    # 全局添加请求钩子，所有服务器的请求都生效， 都会验证当前token.(也可以在需要用到的模块蓝图中单单独添加)
    from comment.utils.request_wares import jwt_request_authorization
    app.before_request(jwt_request_authorization)

    # 加载并注册模块蓝图
    from Shopping.resources.user import user_bp
    app.register_blueprint(user_bp)

    return app
