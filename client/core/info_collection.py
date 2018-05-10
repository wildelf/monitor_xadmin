#date: 2018/4/24
# coding=utf-8

import  platform, socket, time, json, threading
import psutil, schedule, requests
import logging
from conf.setting import *


class InfoCollection():

    # 设置日志
    def log(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=LOG_PATH,
                            filemode='a+')
        return logging.basicConfig


    # 获取位置信息
    def get_location(self,ak):
        location = {}
        my_ip_info = requests.get('https://api.map.baidu.com/location/ip?ak=%s&coor=bd09ll'%ak)
        # print(my_ip_info.text['content']['address_detail'])
        info_dict = my_ip_info.json()
        location['longitude'] = info_dict['content']['point']['y']
        location['latitude'] = info_dict['content']['point']['x']
        location['city'] = info_dict['content']['address_detail']['city']
        return location

    # 获取ip
    def get_ip(self):
        try:
            hostname = socket.getfqdn(socket.gethostname())
            ipaddr = socket.gethostbyname(hostname)
        except Exception as msg:
            print(msg)
            ipaddr = ''
        return ipaddr


    # 获取CPU信息
    def get_cpu_info(self):
        cpu_data = {}
        cpu_times = psutil.cpu_times()
        cpu_data['user'] = cpu_times.user
        cpu_data['system'] = cpu_times.system
        cpu_data['idle'] = cpu_times.idle
        cpu_data['percent'] = psutil.cpu_percent(interval=2)
        return cpu_data

    # 获取内存信息
    def get_mem_info(self):
        mem_data = {}
        mem_info = psutil.virtual_memory()
        mem_data['total'] = mem_info.total
        mem_data['available'] = mem_info.available
        mem_data['percent'] = mem_info.percent
        mem_data['used'] = mem_info.used
        mem_data['free'] = mem_info.free
        mem_data['p_mem'] = self.get_process_mem_info()
        return mem_data

    # 获取进程的pid
    def get_process_pids(self,p_name):
        pid_list = []
        pids = psutil.pids()
        processes = []
        for pid in pids:
            try:
                p = psutil.Process(pid)
                name = p.name()
                processes.append([pid, name])
            except:
                continue

        for p in processes:
            if p[1] == p_name:
                pid_list.append(p[0])

        return pid_list

    # 获取进程的内存信息
    def get_process_mem_info(self):
        pid_list = self.get_process_pids(PROCESS_NAME)
        process_data = []
        percent = 0
        for pid in pid_list:
            p = psutil.Process(pid)
            percent += p.memory_percent()
        process_data.append(PROCESS_NAME)
        process_data.append(percent)
        return process_data

    # 获取磁盘
    def get_disk_info(self):
        disk_data = {'id': [], 'total': [], 'used': [], 'free': [], 'percent': []}
        for id in psutil.disk_partitions():
            if 'cdrom' in id.opts or id.fstype == '':
                continue
            disk_name = id.device.split(':')
            s = disk_name[0]
            disk_data['id'].append(s)
            disk_info = psutil.disk_usage(id.device)
            disk_data['total'].append(round(disk_info.total/1024/1024/1024.0,2))
            disk_data['used'].append(round(disk_info.used/1024/1024/1024.0,2))
            disk_data['free'].append(round(disk_info.free/1024/1024/1024.0,2))
            disk_data['percent'].append(disk_info.percent)
        return disk_data



    # 获取各网卡上传下载信息
    def get_nic(self):

        key_info = psutil.net_io_counters(pernic=True).keys()  # 获取网卡名称

        recv = {}
        sent = {}

        for key in key_info:
            recv.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_recv)  # 各网卡接收的字节数
            sent.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_sent)  # 各网卡发送的字节数

        return key_info, recv, sent

    # 函数计算每秒速率
    def get_nic_rate(self,func):

        key_info, old_recv, old_sent = func()  # 上一秒收集的数据
        time.sleep(1)
        key_info, now_recv, now_sent = func()  # 当前所收集的数据

        net_in = {}
        net_out = {}

        for key in key_info:
            net_in.setdefault(key, (now_recv.get(key) - old_recv.get(key)) / 1024)  # 每秒接收速率
            net_out.setdefault(key, (now_sent.get(key) - old_sent.get(key)) / 1024)  # 每秒发送速率

        return key_info, net_in, net_out

    # 获取网络信息
    def get_net_info(self):
        net_info = []
        key_info, net_in, net_out = self.get_nic_rate(self.get_nic)
        for key in key_info:
            in_data = net_in.get(key)
            out_data = net_out.get(key)
            net_info.append({"nic_name": key, "traffic_in": in_data, "traffic_out": out_data})
        return net_info

    # 数据封装成Json格式
    def get_data_info(self):
        data_info = dict()
        data_info['machine_id'] = MACHINE_ID
        data_info['location'] = self.get_location(AK)
        data_info['hostname'] = platform.node()
        data_info['cpu'] = self.get_cpu_info()
        data_info['mem'] = self.get_mem_info()
        data_info['disk'] = self.get_disk_info()
        data_info['net'] = self.get_net_info()
        return json.dumps(data_info)

    # 发送数据方法
    def post_data(self,url, data):
        print(url)
        try:
            r = requests.post(url, data)
            if r.text:
                logging.info(r.text)
            else:
                logging.info("Server return http status code: {0}".format(r.status_code))
        except Exception as msg:
            logging.info("Server return http status code: {0}".format(r.status_code))
        return True

    # 发送数据
    def agg_info_post(self):

        logging.info('Get the hardwave infos from host:')
        logging.info(self.get_data_info())
        logging.info('----------------------------------------------------------')
        self.post_data("http://{0}:{1}/main/collection/".format(SERVER_IP,SERVER_PORT), self.get_data_info())

        return True

    # 线程方法
    def run_threaded(self,job_func):
        job_thread = threading.Thread(target=job_func)
        job_thread.start()

    # 运行
    def run(self):
        self.log()
        schedule.every(TIMES).seconds.do(self.run_threaded, self.agg_info_post)
        while True:
            schedule.run_pending()
            time.sleep(1)

