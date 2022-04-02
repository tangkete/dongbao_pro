from ronglian_sms_sdk import SmsSDK
import random
"""
    测试短信发送:
    https://www.yuntongxun.com/member/main

"""
class SendMessage:

    accId = '8aaf07087f77bf96017fbbfdeb62213b' #(主账户ID)
    accToken = '2cbae4e8d85c4a2295777389d26fe1b1'
    appId = '8aaf07087f77bf96017fbbfdec652142' #AppID

    def send_message(self, phone):
        sdk = SmsSDK(self.accId, self.accToken, self.appId)
        tid = '1'
        # mobile = '15916413444'
        num = random.randint(1000, 9999)
        datas = (num,'3')
        reps = sdk.sendMessage(tid, phone, datas)
        print(reps)
        print(phone,datas[0])
        return phone,datas[0]

if __name__ == '__main__':
    SendMessage().send_message('15916413444')

