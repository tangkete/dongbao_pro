# -*- coding: utf-8 -*-
from flask import make_response, current_app
from flask_restful.utils import PY3
from json import dumps


# 重写output_json方法
# @api.representation('application/json')
def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""

    # 定义自己的json格式规格
    if 'message' not in data:
        data = {
            'msg':'success',
            'data':data
        }


    settings = current_app.config.get('RESTFUL_JSON', {})

    # If we're in debug mode, and the indent is not set, we set it to a
    # reasonable value here.  Note that this won't override any existing value
    # that was set.  We also set the "sort_keys" value.
    if current_app.debug:
        settings.setdefault('indent', 4)
        settings.setdefault('sort_keys', not PY3)

    # always end the json dumps with a new line
    # see https://github.com/mitsuhiko/flask/pull/1262
    dumped = dumps(data, **settings) + "\n"

    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp
