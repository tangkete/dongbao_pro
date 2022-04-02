# -*- coding: utf-8 -*-
import jwt
import json
from flask import current_app
from jwt import PyJWT, PyJWTError
from comment.models.user import User
from comment.utils import const
from datetime import datetime,timedelta


def jwt_tokens(uid):
    """
    根据已经登录的用户ID生成token
    :param uid: 用户id
    :return:token
    """
    payload = {
        'id':uid,
        # exp代表token的有效时间，而且必须是标准时间值
        'exp': datetime.utcnow() + timedelta(seconds=const.JWT_EXPIRY_SECND)
    }
    # 三个参数：1、字典，uid和有效时间， 2：加密秘钥， 3：哈希算法：默认HS256
    token = jwt.encode(payload=payload, key=const.ACCESS_KEY, algorithm='HS256')
    # current_app.logger.info("jwt_tokens 的token:{}".format(token))
    return token

def verify_tokens(token_str):
    """
    验证token
    :param token_str:
    :return:
    """
    try:
        data = jwt.decode(token_str, key=const.ACCESS_KEY, algorithms='HS256')
        current_app.logger.info('data:{}'.format(data))
    except PyJWTError as e:
        current_app.logger.error(e)
        return {'msg': e}
    user = User.query.filter(User.id == data['id']).first()
    if not user:
        try:
            return
        except Exception as e:
            return {'msg': '{}用户不存在了.e'.format(user.username, e)}
    else:
        if user and user.status != 0: # 如果数据库中存在user这个用户并且状态不是0 的话， 那么账号就是异常 未激活或者过期状态
            return {'msg': '账号过期'}

        return {'id': user.id}
