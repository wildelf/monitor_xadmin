from django.shortcuts import render,HttpResponse
import json
from main import models
# Create your views here.

def get_location():
    device = models.Device.objects.all()[0]
    print(type(device.judge_date._local_timezone()),device.judge_date._local_timezone())

