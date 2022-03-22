# -*- coding: utf-8 -*-
# 负责整个项目的配置信息

class Config:
    """
        配置数据库和SQLAlchemy
    """
    HOSTNAME = '175.178.91.138'
    PORT = '3306'
    DATABASE = 'alembic_test'
    USERNAME = 'root'
    PASSWORD = 'Asd123456'
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4' \
        .format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False # 是否追踪数据库中数据的修改

# 开发环境配置信息
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True # 是否打印SQL语句


# 生产环境配置信息
class ProductConfig(Config):
    DEBUG = False

