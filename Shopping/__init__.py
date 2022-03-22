# -*- coding: utf-8 -*-
from flask import Flask
from settings import map_config


# 创建app对象
def create_app(config_type):
    app = Flask(__name__)
    # 加载项目的配置
    app.config.from_object(map_config.get(config_type))

    # 加载日志处理工具


    # 初始化SQLAlchemy
    from comment.models import db
    db.init_app(app)

    # 加载模块蓝图
    from Shopping.resources.user import user_bp
    app.register_blueprint(user_bp)
    return app
