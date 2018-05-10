from django.http import JsonResponse
import json
# Create your tests here.
#
import requests
#
# AK = 'YN2ajqOcsFnsZI2qbsYulnL6u9iU9dhF'
#
# def get_location(ak):
#     location = {}
#     my_ip_info = requests.get('https://api.map.baidu.com/location/ip?ak=%s'%ak)
#     # print(my_ip_info.text['content']['address_detail'])
#     info_dict = my_ip_info.json()
#     print(info_dict)
#     location['longitude'] = round(float(info_dict['content']['point']['y'])/100000,2)
#     location['latitude'] = round(float(info_dict['content']['point']['x'])/100000,2)
#     location['city'] = info_dict['content']['address_detail']['city']
#     return location
#
#
# if __name__ == '__main__':
#     location = get_location(AK)
#     print(location)

# 发送信息
def send_message(phone_num):
    result = \
    requests.get('http://www.wxeshop.com/wxclient/sendverifycode/', params={'phonenum': phone_num, 'code': 'hello'})
    # print(result.content)
    return result.text

a = send_message(18718681396)
print(a)