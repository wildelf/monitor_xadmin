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
        received_json_data['timestamp'] = int(time.time())
        client = pymongo.MongoClient(MONGO_URL,MONGO_PORT)
        db = client[MONGO_DB]
        collection = db[machine_id]
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

