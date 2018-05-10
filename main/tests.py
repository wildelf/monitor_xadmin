from django.test import TestCase

# Create your tests here.

import requests

AK = 'YN2ajqOcsFnsZI2qbsYulnL6u9iU9dhF'

def get_location(ak):
    location = {}
    my_ip_info = requests.get('https://api.map.baidu.com/location/ip?ak=%s'%ak)
    # print(my_ip_info.text['content']['address_detail'])
    info_dict = my_ip_info.json()
    location['longitude'] = round(float(info_dict['content']['point']['y'])/100000,2)
    location['latitude'] = round(float(info_dict['content']['point']['x'])/100000,2)

    return location


if __name__ == '__main__':
    location = get_location(AK)
    print(location)
