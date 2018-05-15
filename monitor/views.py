import json
import time
from django.shortcuts import render,HttpResponse
from main import models
from monitor.api import GetSysData

TIME_SECTOR = (
            3600,
            3600*3,
            3600*5,
            86400,
            86400*3,
            86400*7,
)


# 返回首页
def index(request):
    all_host = models.Device.objects.all()
    return render(request,'monitor/index.html',locals())

# 机器系统信息
def host_info(request,machine_id,timing):

    # 传递磁盘号给前端JS,用以迭代分区图表
    disk = GetSysData(machine_id, "disk", 3600, 1)
    disk_data = disk.get_data()
    partitions_len = []
    for d in disk_data:
        p = len(d['disk']['id'])
        for x in range(p):
            partitions_len.append(x)

    # 传递网卡号给前端,用以迭代分区图表
    net = GetSysData(machine_id, "net", 3600, 1)
    nic_data = net.get_data()
    nic_len = []
    for n in nic_data:
        p = len(n["net"])
        for x in range(p):
            nic_len.append(x)

    return render(request, "monitor/host_info_{}.html".format(timing), locals())

# 从mongodb动态获取cpu数据
def get_cpu(request, machine_id, timing):
    data_time = []
    cpu_percent = []
    range_time = TIME_SECTOR[int(timing)]
    cpu_data = GetSysData(machine_id, "cpu", range_time)
    for doc in cpu_data.get_data():
        unix_time = doc['timestamp']
        times = time.localtime(unix_time)
        dt = time.strftime("%m-%d %H:%M", times)
        data_time.append(dt)
        c_percent = doc['cpu']['percent']
        cpu_percent.append(c_percent)
    data = {"data_time": data_time, "cpu_percent": cpu_percent}
    return HttpResponse(json.dumps(data))

# 从mongodb动态获取内存数据
def get_mem(request, machine_id, timing):
    data_time = []
    mem_percent = []
    pro_percent = []
    pro_name = ''
    range_time = TIME_SECTOR[int(timing)]
    mem_data = GetSysData(machine_id, "mem", range_time)
    for doc in mem_data.get_data():
        unix_time = doc['timestamp']
        times = time.localtime(unix_time)
        dt = time.strftime("%m-%d %H:%M", times)
        data_time.append(dt)
        m_percent = doc['mem']['percent']
        mem_percent.append(m_percent)

        p_percent = doc['mem']["p_mem"][1]
        pro_name = doc['mem']["p_mem"][0]
        pro_percent.append(p_percent)
    data = {"data_time": data_time, "mem_percent": mem_percent,"pro_percent":pro_percent,'pro_name':pro_name}
    return HttpResponse(json.dumps(data))


# # 从mongodb动态获取进程内存数据
# def get_pro_mem(request, machine_id, timing):
#     data_time = []
#     pro_percent = []
#     pro_name = ''
#     range_time = TIME_SECTOR[int(timing)]
#     mem_data = GetSysData(machine_id, "p_mem", range_time)
#     for doc in mem_data.get_data():
#         unix_time = doc['timestamp']
#         times = time.localtime(unix_time)
#         dt = time.strftime("%m-%d %H:%M", times)
#         data_time.append(dt)
#         p_percent = doc["p_mem"][1]
#         pro_name = doc["p_mem"][0]
#         pro_percent.append(p_percent)
#     data = {"data_time": data_time, "pro_name":pro_name,"pro_percent": pro_percent}
#     return HttpResponse(json.dumps(data))


# 从mongodb动态获取磁盘数据
def get_disk(request, machine_id, timing):
    data_time = []
    disk_name_list = []
    disk_percent_list = []
    range_time = TIME_SECTOR[int(timing)]
    disk = GetSysData(machine_id, "disk", range_time)
    for doc in disk.get_data():
        unix_time = doc['timestamp']
        times = time.localtime(unix_time)
        dt = time.strftime("%m-%d %H:%M", times)
        data_time.append(dt)

        disk_name_list = doc['disk']['id']
        if not disk_percent_list:
            for i in range(len(doc['disk']['percent'])):
                disk_percent_list.append([])
        for i in range(len(doc['disk']['percent'])):
            disk_percent_list[i].append(doc['disk']['percent'][i])


    data = {"data_time": data_time, "disk_name_list":disk_name_list,"disk_percent_list":disk_percent_list}
    return HttpResponse(json.dumps(data))

# 从mongodb动态获取网络数据
def get_net(request, machine_id, timing):
    data_time = []
    nic_in = []
    nic_out = []
    nic_name = ""
    range_time = TIME_SECTOR[int(timing)]
    net = GetSysData(machine_id, "net", range_time)
    for doc in net.get_data():
        unix_time = doc['timestamp']
        times = time.localtime(unix_time)
        dt = time.strftime("%m-%d %H:%M", times)
        data_time.append(dt)
        in_ = 0
        out_ = 0
        for i in range(len(doc['net'])):
            in_ += doc['net'][i]['traffic_in']
            out_ += doc['net'][i]['traffic_out']
        nic_in.append(in_)
        nic_out.append(out_)

    data = {"data_time": data_time, "nic_name": nic_name, "traffic_in": nic_in, "traffic_out": nic_out}
    return HttpResponse(json.dumps(data))


