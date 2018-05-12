#date: 2018/5/12
from __future__ import absolute_import, unicode_literals
import time
import json
import requests
from celery import shared_task
from main import models,api


# 发送信息
@shared_task
def send_message(device_id,phone_num,code):
    result = \
    requests.get('http://www.wxeshop.com/wxclient/sendverifycode/', params={'phonenum': phone_num, 'code': code})
    # print(result.content)
    res = json.loads(result.text)
    status = res.get('result')

    if status==0:
        obj = models.Device.objects.filter(id=device_id)
        obj.update(send_message=0)
    print(type(status), status)

# 检测设备状态
@shared_task
def judge_device_status():
    print('开始检测')
    '''检测设备状态机制'''
    all_devices = models.Device.objects.all()
    for device in all_devices:
        obj = models.Device.objects.filter(id=device.id)
        mobile = device.user.mobile
        cursor = api.get_check_data(device.deviceid)
        if cursor.count():
            if api.get_pre_check_data(device.deviceid).count():
                '''该设备正常连接'''
                obj.update(send_message=1,status=1,judge_date=time.strftime('%Y-%m-%d %H:%M',time.localtime()))
            else:
                if device.status == 0:
                    '''新设备首次上线'''
                    obj.update(judge_date=time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                    '''发短信通知'''
                    send_message.delay(device.id,mobile,'新设备')
                else:
                    '''离线重连'''
                    obj.update(status=2,judge_date=time.strftime('%Y-%m-%d %H:%M',time.localtime()))
                    '''发短信通知'''
                    send_message.delay(device.id,mobile,'离线重连')
        else:
            '''该设备离线'''
            obj.update(status=3,judge_date=time.strftime('%Y-%m-%d %H:%M',time.localtime()))
    print('检测结束')


