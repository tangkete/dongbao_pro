# -*- coding: utf-8 -*-
from urllib import parse

# 负责整个项目的配置信息
class Config:
    """
        配置数据库和SQLAlchemy
    """
    HOSTNAME = '175.178.91.138'
    PORT = '3306'
    DATABASE = 'MYDB'
    USERNAME = 'root'
    PASSWORD = '!Asd123456@...'
    PWD = parse.quote_plus(PASSWORD) # 因为密码带@ 特殊符号， 所以需要使用quote_plus进行编码
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4' \
        .format(USERNAME, PWD, HOSTNAME, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False # 是否追踪数据库中数据的修改


    # 日志配置
    LOGGING_LEVEL = 'INFO'  #级别
    LOGGING_FILE_DIR = 'logs/'  # 路径
    LOGGING_FILE_MAX_BYTES = 300 * 1024 * 1024  # 最大日志文件大小
    LOGGING_FILE_BACKUP = 30  # 备份日志个数


    # 限流器采用Redis保存数据，需要安装flask-redis， 使用实例0
    RATELIMIT_STORAGE_URL = 'redis://175.178.91.138:30333/0'
    # 限流策略：移动窗口，时间窗口会自动变化
    RATELIMIT_STRATEGY = 'moving-window'

    # redis数据库的链接地址， 使用实例1 来存放缓存数据， 包括短信验证码
    REDIS_URL = 'redis://175.178.91.138:30333/1'



# 开发环境配置信息
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False  # 是否打印SQL语句


# 生产环境配置信息
class ProductConfig(Config):
    DEBUG = False

