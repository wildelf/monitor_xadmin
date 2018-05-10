#date: 2018/5/10

import threading
import time
import schedule
from main import models,api
from main.config import *

# 检测设备状态
def judge_device_status():

    print('开始检测')
    '''检测设备状态机制'''
    all_devices = models.Device.objects.all()
    for device in all_devices:
        obj = models.Device.objects.filter(id=device.id)
        cursor = api.get_check_data(device.deviceid)
        if cursor.count():
            if api.get_pre_check_data(device.deviceid).count():
                '''该设备正常连接'''
                obj.update(status=1,judge_date=time.strftime('%Y-%m-%d %H:%M',time.localtime()))
            else:
                if obj[0].status == 0:
                    '''新设备首次上线'''
                    obj.update(judge_date=time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                    '''发短信通知'''
                    pass
                else:
                    '''离线重连'''
                    obj.update(status=2,judge_date=time.strftime('%Y-%m-%d %H:%M',time.localtime()))
                    '''发短信通知'''
        else:
            '''该设备离线'''
            obj.update(status=3,judge_date=time.strftime('%Y-%m-%d %H:%M',time.localtime()))
    print('检测结束')


# 线程方法
def run_threaded(func):
    job_thread = threading.Thread(target=func)
    job_thread.start()

# 运行
def run():
    schedule.every(JUDGE_TIMES).seconds.do(run_threaded, judge_device_status)
    while True:
        schedule.run_pending()
        time.sleep(1)

