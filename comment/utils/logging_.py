# -*- coding: utf-8 -*-
import logging
from logging import handlers
from flask import request
import os


class RequestShoppingFormatter(logging.Formatter):
    """
     自定义日志输出格式
    """
    def format(self, record):
        record.url = request.url # 日志中定义请求地址
        record.remote_addr = request.remote_addr # 日志中记录客户端地址
        return super().format(record)


# 创建一个日志函数
def logger(app):
    """
    设置日志配置
    :param app: Flask 中的app对象
    :return:
    """
    logging_level = app.config['LOGGING_LEVEL']
    logging_file_dir = app.config['LOGGING_FILE_DIR']
    logging_file_max_bytes = app.config['LOGGING_FILE_MAX_BYTES']
    logging_file_backup = app.config['LOGGING_FILE_BACKUP']

    # 设置日志输出格式:时间、（客户端请求地址， 请求url：类中自定义）、日志级别，模块 行号 日志信息
    request_formatter = RequestShoppingFormatter(
        '[%(asctime)s] %(remote_addr)s  请求 %(url)s \t %(levelname)s , %(module)s %(lineno)d line : %(message)s')
    if os.path.isdir(logging_file_dir):
        pass
    else:
        os.mkdir(logging_file_dir)

    # 自定义目录和日志文件
    flask_file_handler = logging.handlers.RotatingFileHandler(filename=os.path.join(logging_file_dir, 'shopping.log'),
                                         maxBytes=logging_file_max_bytes,
                                         backupCount=logging_file_backup)
    # 给当前handle设置格式
    flask_file_handler.setFormatter(request_formatter)
    # 得到一个logger对象
    flask_logger = logging.getLogger('Shopping')
    flask_logger.addHandler(flask_file_handler)
    flask_logger.setLevel(logging_level)

    flask_console_handler = logging.StreamHandler()
    flask_console_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s %(module)s  %(lineno)d : %(message)s'))
    # 当前项目运行环境是DEBUG模式，才使用控制台
    if app.debug:
        flask_logger.addHandler(flask_console_handler)
