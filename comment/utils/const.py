# -*- coding: utf-8 -*-
import os

# ACCESS_KEY_ID/ACCESS_KEY_SECRT 根据实际申请的账号信息进行替换
# AccessKeyId 用于标识用户
ACCESS_KEY_ID = ""
ACCESS_KEY_SECRT = ""


ACCESS_KEY = os.urandom(16) # 生成16位的随机数
JWT_EXPIRY_SECND = 60*60 # token的有效时间
