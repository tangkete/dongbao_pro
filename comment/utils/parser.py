# -*- coding: utf-8 -*-
import re

def mobile(mobile_str):
    """
    验证手机号格式
    :param mobile_str:str 被检验的字符串
    :return:
    """
    if re.match(r'^1[3-9]\d{9}$', mobile_str):
        return mobile_str
    else:
        raise ValueError('{} is not a valid mobile'.format(mobile_str))


def regex(pattern):
    """
    正则校验函数，闭包
    :param pattern: str正则表达式
    :return: 返回一个函数
    """
    def validate(value_str):
        """
        具体校验字符串，根据自定义正则表达式
        :param value_str:
        :return:
        """
        if re.match(pattern, value_str):
            return value_str
        else:
            raise ValueError('{} is a valid code.'.format(value_str))
    return validate

def email(email_str):
    """
    验证邮箱格式
    :param email_str:str 被检验的字符串
    :return:
    """
    if re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email_str):
        return email_str
    else:
        raise ValueError('{} is not a valid email'.format(email_str))

