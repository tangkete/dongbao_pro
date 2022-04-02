# -*- coding: utf-8 -*-
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from Shopping import create_app
from comment.models import db
"""
    1、对数据库表的操作
"""
# 初始化app
app = create_app('develop')
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    """
        执行命令：
        python3 t_Migrate.py db init
        python3 t_Migrate.py db migrate
        python3 t_Migrate.py db upgrade
    """
    manager.run()

