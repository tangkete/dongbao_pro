# -*- coding: utf-8 -*-
# 存放常量
# 根据手机号码限制短信验证码发生的频次，
LIMIT_SMS_CODE_BY_MOBILE = '1/minute' # 1分钟一次

# 根据客户端IP限制短信验证码发送的频次
LIMIT_SMS_CODE_BY_IP = '10/hour'

# 短信验证码存放在redis 的失效, 以秒为单位
SMS_CODE_EXPIRES = 5 * 60
