#date: 2018/5/10

import threading
import time
from main import models,api
from main.config import *


# 线程方法
def run_threaded(self,job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

# 检测设备状态
def judge_device_status(times):
    while True:
        '''检测设备状态机制'''
        all_devices = models.Device.objects.all()
        for device in all_devices:
            cursor = api.get_check_data(device.deviceid)
            if cursor.count():

                print('存在数据')
                if api.get_pre_check_data(device.deviceid).count():
                    print('该机器正常')
                else:
                    print('该机器重连或是新机器')
            else:
                models.Device.objects.filter(id=device.id).update(status=3, judge_date=time.strftime('%Y-%m-%d %H:%M',
                                                                                                time.localtime()))

        time.sleep(times)