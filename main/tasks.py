#date: 2018/5/12
from __future__ import absolute_import, unicode_literals
import time
import json
import requests
from celery import shared_task
from main import models,api


# 发送信息
@shared_task
def send_message(phone_num,message,device_id=0):

    result = \
    requests.get('http://www.wxeshop.com/wxclient/sendverifycode/', params={'phonenum': phone_num, 'code': message})
    res = json.loads(result.text)
    status = res.get('result')

    if device_id:
        if status==0:
            obj = models.Device.objects.filter(id=device_id)
            obj.update(send_message=0)


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
                    '''发短信通知用户'''
                    send_message.delay(mobile,'新设备',device.id,)
                    '''发短信通知经销商'''
                    send_message.delay(device.user.parent.mobile,'新设备')
                else:
                    '''离线重连'''
                    obj.update(status=2,judge_date=time.strftime('%Y-%m-%d %H:%M',time.localtime()))
                    '''发短信通知用户'''
                    send_message.delay(mobile, '离线重连', device.id)
                    '''发短信通知经销商'''
                    send_message.delay(device.user.parent.mobile, '离线重连')
        else:
            '''该设备离线'''
            obj.update(status=3,judge_date=time.strftime('%Y-%m-%d %H:%M',time.localtime()))
    print('检测结束')


# 记录和通知设备信息
@shared_task
def check_device():
    all_devices = models.Device.objects.all()
    for device in all_devices:
        if device.status == 3:
            '''设备离线'''
            user = device.user
            '''发送信息'''
            while user:
                send_message.delay(user.mobile, '设备离线')
                '''记录短信信息'''
                models.MessageLog.objects.create(
                    date=time.strftime('%Y-%m-%d %H:%M', time.localtime()),
                    user = user,
                    message = '设备离线'
                )
                user = user.parent
            '''记录信息'''
            models.CheckLog.objects.create(
                date = time.strftime('%Y-%m-%d %H:%M', time.localtime()),
                device = device,
                status = 1
            )
        else:
            '''记录信息'''
            models.CheckLog.objects.create(
                date=time.strftime('%Y-%m-%d %H:%M', time.localtime()),
                device=device,
                status=0
            )