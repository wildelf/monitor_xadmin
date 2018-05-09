from django.shortcuts import render,HttpResponse

# Create your views here.
import json


def get_location(request):
    data = {'location':[[114.1333,22.5333,'M-001','深圳','正常','否','2018-5-9','正常'],\
                        [115.1333,28.5333,'M-002','陕西','新设备','是','2018-5-9','重登/新设备']]}
    return HttpResponse(json.dumps(data))
