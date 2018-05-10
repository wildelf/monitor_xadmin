from django.shortcuts import render,HttpResponse

# Create your views here.
import json
from main import models

# 获取设备位置信息
def get_location(request):
    all_devices = models.Device.objects.all()
    data = []
    for device in all_devices:
        device_data = []
        device_data.append(device.latitude)
        device_data.append(device.longitude)
        device_data.append(device.deviceid)
        device_data.append(device.location)
        device_data.append(device.get_status_display())
        device_data.append(device.get_send_message_display())
        device_data.append(str(device.judge_date)[:-9])
        if device.status==0 or device.status==2:
            device_data.append('重登/新设备')
        elif device.status==1:
            device_data.append('正常')
        else:
            device_data.append('离线')

        data.append(device_data)

    # data = {'location':[[114.1333,22.5333,'M-001','深圳','正常','否','2018-5-9','正常'],\
    #                     [115.1333,28.5333,'M-002','陕西','新设备','是','2018-5-9','重登/新设备']]}
    return HttpResponse(json.dumps(data))
