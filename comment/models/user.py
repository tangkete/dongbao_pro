# -*- coding: utf-8 -*-
from comment.models import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
"""
    用户模型类
"""
class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True, doc='用户id')
    username = db.Column(db.String(64), unique=True, doc='用户名')
    # 数据库中存放的是加密后的密文，采用flask提供的哈希算法,长度128位的密文
    password = db.Column(db.String(128), doc='密码')
    icon = db.Column(db.String(3000), doc='用户头像图片')
    email = db.Column(db.String(100), unique=True, doc='邮箱')
    nick_name = db.Column(db.String(55), doc='昵称')
    note = db.Column(db.String(500), doc='备注')
    phone = db.Column(db.String(11), unique=True, doc='手机号')

    login_time = db.Column(db.DateTime, default=datetime.now(),doc='登录时间')
    create_time = db.Column(db.DateTime, default=datetime.now(),doc='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), doc='修改时间')
    status = db.Column(db.Integer, doc='用户状态') # 0代表正常

    # pwd属性get函数，获取
    @property
    def pwd(self):
        return self.password

    # 属性get函数
    @pwd.setter
    def pwd(self, x_password):
        """
        根据明文的密码，转换成哈希值密文
        :param x_password:明文密码
        :return:加密后的密文
        """
        self.password = generate_password_hash(x_password) # 加密成密文

    def check_password(self, x_password):
        """
        验证密码是否加密
        :param x_password:输入明文
        :return:true/false
        """
        return check_password_hash(self.password, x_password)

    # @property
    # def mobile(self):
    #     return self.phone
    # @mobile.setter
    # def mobile(self, x_phone):
    #     self.phone = generate_password_hash(x_phone)

