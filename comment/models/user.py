# -*- coding: utf-8 -*-
from comment.models import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), doc='用户名')
    password = db.Column(db.String(64), doc='密码')
    icon = db.Column(db.String(5000), doc='用户头像图片')
    email = db.Column(db.String(100), doc='邮箱')
    nick_name = db.Column(db.String(200), doc='昵称')
    note = db.Column(db.String(500), doc='备注')
    phone = db.Column(db.String(11), doc='手机号')

    login_tim = db.Column(db.DateTime, default=datetime.now(),doc='登录时间')
    create_time = db.Column(db.DateTime, default=datetime.now(),doc='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), doc='创建时间')
    status = db.Column(db.Integer, doc='用户状态')


