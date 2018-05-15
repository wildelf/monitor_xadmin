from django.urls import path, include, re_path
from monitor import views

urlpatterns = [
    re_path(r'^index/$', views.index, name='sys_data_index'),
    re_path(r'^system/(?P<machine_id>.+)/(?P<timing>\d+)/$', views.host_info, name='host_info'),
    re_path(r'^get/cpu/(?P<machine_id>.+)/(?P<timing>\d+)/$', views.get_cpu, name='get_cpu'),
    re_path(r'^get/mem/(?P<machine_id>.+)/(?P<timing>\d+)/$', views.get_mem, name='get_mem'),
    # url(r'^get/pro/mem/(?P<machine_id>.+)/(?P<timing>\d+)/$', views.get_pro_mem, name='get_pro_mem'),
    re_path(r'^get/disk/(?P<machine_id>.+)/(?P<timing>\d+)/$', views.get_disk, name='get_disk'),
    re_path(r'^get/net/(?P<machine_id>.+)/(?P<timing>\d+)/$', views.get_net, name='get_net'),
]
