# -*- coding: utf-8 -*-
from Shopping import create_app
from flask_script import Manager
# from comment.models import db
from flask_sqlalchemy import SQLAlchemy

# 定义app
app = create_app('develop')
# 定义db
db = SQLAlchemy(app)
# 定义manager
manager = Manager(app)

class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uname = db.Column(db.String(32), nullable=False)
    pwd = db.Column(db.String(32), nullable=False)


# db.create_all()

# 通过命令创建一个用户,要传参数,使用option

# 通过命令行执行：python3 t_comment.py create_user -u cott -p 123123
@manager.option("-u", "--uname", dest="uname") # dest跟函数中的形参值一致
@manager.option("-p", "--pwd", dest="pwd")
def create_user(uname, pwd):
    user = User(uname=uname, pwd=pwd)
    db.session.add(user)
    db.session.commit()
    print("{}插入成功".format(uname))


@manager.command
def hello():
    print('命令执行成功!!')


if __name__ == '__main__':
    # app.run()
    manager.run()
