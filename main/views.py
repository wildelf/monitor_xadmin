from django.shortcuts import render,HttpResponse
import json
import pytz
from main import models
# Create your views here.


# 获取设备位置信息
def get_location(request):
    all_devices = models.Device.objects.all()
    data = []
    tz = pytz.timezone('Asia/Shanghai')
    for device in all_devices:
        device_data = []
        device_data.append(device.latitude)
        device_data.append(device.longitude)
        device_data.append(device.deviceid)
        device_data.append(device.location)
        device_data.append(device.get_status_display())
        device_data.append(device.get_send_message_display())
        date = device.judge_date.astimezone(tz)
        device_data.append(str(date)[:-9])
        print(type(device.judge_date))
        if device.status==0 or device.status==2:
            device_data.append('重登/新设备')
        elif device.status==1:
            device_data.append('正常')
        else:
            device_data.append('离线')

        data.append(device_data)

    return HttpResponse(json.dumps(data))


