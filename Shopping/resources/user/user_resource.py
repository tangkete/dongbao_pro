# -*- coding: utf-8 -*-
import random
from flask_restful import Resource
from ronglian_sms_sdk import SmsSDK
from comment.utils.decorators import login_required
from comment.utils.limiter import limiter as lmt
from comment.models.user import User
from flask import current_app, request, g
from . import constants
from flask_limiter.util import get_remote_address
import json
from comment.utils.shopping_redis import redis_client
from flask_restful.reqparse import RequestParser
from comment.utils import parser
from comment.models import db
from comment.utils.tokens_jwt import jwt_tokens, verify_tokens


# 定义资源类
class Shopping_user(Resource):
    """
        在get函数里，加上登录的拦截
    """
    method_decorators = {
        'get': [login_required],
        'post': [login_required]
    }
    def get(self): # 测试：当前get函数必须要登录后才能访问
        current_app.logger.info("测试日志输出")
        # 可能需要用到User模型类
        # 返回json对象
        return {'hello':'测试'}

    def post(self):
        return {'msg': 'hello post测试'}

    def put(self):
        return {'msg': 'hello put测试'}

class SendMessage(Resource):
    """
        获取手机验证码
    """
    # get_remote_address 获取客户端远程ip地址
    error_message = 'To many requests.'
    decorators = [
        # 限流器参数3个
        # 1、限流的速率
        # 2、key_func,对象， 手机号码或者ip
        # 3、超出频次之后的错误提示
        lmt.limit(constants.LIMIT_SMS_CODE_BY_MOBILE,
                  key_func=lambda: request.args['phone'],
                  # key_func=request.args('phone'),
                  error_message=error_message),
        lmt.limit(constants.LIMIT_SMS_CODE_BY_IP,
                  key_func=get_remote_address,
                  error_message=error_message)
    ]
    accId = '8aaf07087f77bf96017fbbfdeb62213b'  # (主账户ID)
    accToken = '2cbae4e8d85c4a2295777389d26fe1b1'
    appId = '8aaf07087f77bf96017fbbfdec652142'  # AppID

    def get(self):
        sdk = SmsSDK(self.accId, self.accToken, self.appId)
        tid = '1'
        # phone = '15916413444'
        phone = request.args.get('phone').strip()
        code = random.randint(1000, 9999)
        datas = (code, '3')
        result = sdk.sendMessage(tid, phone, datas) # 返回的是json字符串
        result = json.loads(result)  # 将字符串转为字典
        # print(type(result))
        # 将手机号码添加到result响应结果里面
        result['phone'] = phone
        result['data_code'] = code

        # 短信验证码发送成功后续存放在redis数据库中，有效时长为5分钟
        # setex传三个参数，参数1：key， 参数2：时长 ， 参数三: value
        redis_client.setex('shopping:code:{}'.format(phone),
                         constants.SMS_CODE_EXPIRES, code)
        return result

class AuthorizationCodeResource(Resource):
    """
        校验验证码
        提交手机号和验证码，开始验证
    """
    def post(self):
        # RequestParser对象用来检验和转换请求数据
        rp = RequestParser()
        # required代表必须验证, type指定验证方法
        rp.add_argument('phone', type=parser.mobile, required=True)
        rp.add_argument('code', type=parser.regex(r'^\d{4}$'), required=True)
        args = rp.parse_args()
        phone = args.phone
        code = args.code
        # 从redis 数据库中得到之前保存的验证码
        key = 'shopping:code:{}'.format(phone)
        try:
            real_code = redis_client.get(key) # 从redis中返回的是字节数据
        except ConnectionError as e:
            current_app.logger.error(e)
            return {'message':'redis db connect error...'}, 400
        # 开始校验
        if not real_code or real_code.decode() != code:
            return {'message':'验证码错误或已失效.'}, 400
        return {'phone':phone, 'msg':'code success.'}

class RegisterUserResource(Resource):
    """
        注册
    """
    def post(self):
        rp = RequestParser()
        # required代表必须验证, type指定验证方法:正则表达式, help是报错时候错误信息
        rp.add_argument('username', required=True, help='missing a username')
        rp.add_argument('password', required=True)
        rp.add_argument('phone', type=parser.mobile, required=True)
        rp.add_argument('email', type=parser.email, required=True)
        rp.add_argument('note', required=False, help='check param note')
        # 从请求中获取所有参数，用args接收
        args = rp.parse_args()
        username = args.username
        password = args.password
        phone = args.phone
        email = args.email

        # 验证用户名和邮箱是否已经注册，从mysql中根据用户名、邮箱查询
        uname = User.query.filter(User.username == username).first()
        uemail = User.query.filter(User.email == email).first()
        uphone = User.query.filter(User.phone == phone).first()
        if uname:
            current_app.logger.info('{}用户已经存在'.format(username))
            return {'message':'The username alerady exists.'}, 400
        if uemail:
            current_app.logger.info('{}邮箱已注册'.format(email))
            return {'message':'The email alerady exists.'}, 400
        if uphone:
            current_app.logger.info('{}手机已经注册.'.format(phone))
            return {'message': 'The phone alerady exists.'}, 400
        # 如果不存在则将用户信息保存到数据库中, 密码要加密
        # 要传User中加密校验的参数pwd,不能传password
        u = User(username=username, phone=phone, pwd=password, email=email, status=0)
        db.session.add(u)
        db.session.commit()
        return {'msg':'OK'}

class UpdateUserResource(Resource):
    """
        修改登录用户信息
    """
    def put(self):
        rp = RequestParser()
        rp.add_argument('username', required=True, help='missing username param! ')
        rp.add_argument('note', required=False)
        rp.add_argument('icon', type=parser.regex('(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]'),required=False)
        rp.add_argument('nick_name', required=False)



class UserLoginResource(Resource):
    """
        登录
    """
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')

        if not any([username, password]): # 如果username 或者 password不存在
            return {'message':'用户名或者密码不允许为空.'}, 400

        user = User.query.filter(User.username == username).first()
        if user:
            if user.check_password(password):
                # 把登录成功后的用户id 得到token，token返回给前端
                token = jwt_tokens(user.id)
                # verify_tokens(token)
                return {'msg': 'Login Success.', 'token': token, 'user_id': user.id, 'username': user.username}, 200

        return {'message': '用户名或者密码错误'}, 400

class UserLoginOutResource(Resource):
    """
    退出登录
    """
    def post(self):
        if g.user_id:
            g.user_id = None
        return {"msg": "退出登录"} ,200

class IsExistPhoneResource(Resource):
    """
        判断手机号码是否存在
    """
    def post(self):
        phone = request.form.get('phone')
        if len(phone) == 11 and phone.isdigit() and phone[0].isdigit():
            user = User.query.filter(User.phone == phone).first()
            if user:
                current_app.logger.info('{}手机号码已注册,{}'.format(phone, type(phone)))
                # 因为返回有message ，所以不需要用到output_json 封装
                return {'code': 203, 'isExist': True, 'message': '手机号码已经注册'}
            return {'msg':'手机号可以注册'}
        else:
            return {'code': 201, 'message': '请输入11位数的手机号码'}

