import json
import requests
# 发送信息
def send_message(phone_num):
    result = \
    requests.get('http://www.wxeshop.com/wxclient/sendverifycode/', params={'phonenum': phone_num, 'code': '你好'})
    return result.text

for i in range(10):
    send_message('18718681396')

