#date: 2018/5/10

import threading
import time
from main.config import *


# 线程方法
def run_threaded(self,job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

# 检测设备状态
def judge_device_status(times):
    while True:
        '''检测设备状态机制'''
        time.sleep(times)