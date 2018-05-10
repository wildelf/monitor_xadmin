#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
import time
import pymongo
from main.config import *
from main import models
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# 接受客户端数据
@csrf_exempt
def received_sys_info(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body.decode('utf-8'))
        machine_id = received_json_data["machine_id"]
        obj = models.Device.objects.filter(deviceid=machine_id)
        if not obj:
            return HttpResponse('该设备编号未注册')
        if not obj[0].longitude:
            lng = received_json_data['location']['longitude']
            lat = received_json_data['location']['latitude']
            city = received_json_data['location']['city']
            obj.update(longitude=lng,latitude=lat,location=city)
        received_json_data['timestamp'] = int(time.time())
        collection = connect_mongo(machine_id)
        collection.insert_one(received_json_data)
        return HttpResponse("Post the system Monitor Data successfully!")
    else:
        return HttpResponse("Your push have errors, Please Check your data!")


# 发送信息
def send_message(phone_num):
    result = \
    requests.get('http://www.wxeshop.com/wxclient/sendverifycode/', params={'phonenum': phone_num, 'code': 'hello'})
    # print(result.content)
    return JsonResponse(json.loads(result.content.decode('utf-8')), safe=False)

# 连接mongo
def connect_mongo(db_name):
    client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
    db = client[MONGO_DB]
    collection = db[db_name]
    return collection

# 获取检测时间内的数据
def get_check_data(device_id):
    collection = connect_mongo(device_id)
    now_time = int(time.time())
    find_time = now_time - JUDGE_TIMES
    cursor = collection.find({'timestamp': {'$gt': find_time}}, {"timestamp": 1}).limit(0)
    return cursor

# 获取上一个检测时间内的数据
def get_pre_check_data(device_id):
    collection = connect_mongo(device_id)
    now_time = int(time.time())
    start_find_time = now_time - JUDGE_TIMES*2
    end_find_time = now_time - JUDGE_TIMES
    cursor = collection.find({'timestamp': {'$gt': start_find_time,'$lte':end_find_time}}, {"timestamp": 1}).limit(0)
    return cursor