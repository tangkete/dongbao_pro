# -*- coding: utf-8 -*-
import os
import sys
# sys.path.append(os.path.dirname(__file__))
from Shopping import create_app
from settings import map_config

app = create_app('develop')

if __name__ == '__main__':
    app.run()
