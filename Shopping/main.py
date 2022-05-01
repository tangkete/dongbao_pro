# -*- coding: utf-8 -*-
import os
import sys
from Shopping import create_app

path = os.path.dirname(sys.path[0]) # 得到当前项目绝对路径
if path and path not in sys.path:
    sys.path.append(path) # 把当前项目的路径追加到系统环境变量中


app = create_app('develop')

if __name__ == '__main__':
    app.run(debug=True)
