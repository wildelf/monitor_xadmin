#! -*- coding:utf-8 -*-
import datetime
import logging

from django.contrib.auth.models import Group, Permission, User
from django.db import connection
from django.db.models import Count
from django.forms import Media
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _, ugettext

import socket

from main.models import SiteUser, SiteGroup, SitePermission,Device

from xadmin.models import Log
import xadmin
from xadmin.plugins.auth import UserAdmin, GroupAdmin
from xadmin.views import CommAdminView

logger = logging.getLogger(__name__)


class GlobalSetting(object):
    menu_style = 'accordion'  # 'default'#default'#'accordion'
    show_bookmarks = False
    site_title = u'WIN10设备监测系统管理后台'
    site_footer = u'深圳市金未来信息技术有限公司'
    system_version = "V1.0"
    global_add_models = []
    enable_themes = True
    use_bootswatch = True

    # @property
    # def site_title(self):
    #     try:
    #         user = self.request.user
    #         if user.is_authenticated():
    #             if user.haslevel2 and user.platform_admin.all().count()>0:
    #                 return self.site_title_global+"（"+user.platform_admin.all()[0].name+"）"
    #     except Exception as ex:
    #         pass
    #
    #     return self.site_title_global

    def get_site_menu(self):
        return (
            {'title': '工作台', 'url': '/xadmin/', 'icon': 'shouye'},

            {'title': '实时监控', 'icon': 'fa fa-list', 'menus': (

            )},

            {'title': '历史查询', 'icon': 'fa fa-list', 'menus': (

            )},


            {'title': '系统管理', 'icon': 'fa fa-gear', 'menus': (
                {'title': '用户', 'perm': self.get_model_perm(SiteUser, 'view'), 'icon': 'fa fa-user',
                 'url': self.get_model_url(SiteUser, 'changelist')},
                {'title': '角色', 'perm': self.get_model_perm(SiteGroup, 'view'), 'icon': 'fa fa-users',
                 'url': self.get_model_url(SiteGroup, 'changelist')},
                # {'title': '角色', 'perm': self.get_model_perm(Permission, 'view'), 'icon': 'fa fa-lock',
                #  'url': self.get_model_url(Permission, 'changelist')},
                {'title': '权限', 'perm': self.get_model_perm(SitePermission, 'view'), 'icon': 'fa fa-lock',
                 'url': self.get_model_url(SitePermission, 'changelist')},

            )},
            {'title': '日志管理', 'icon': 'fa fa-ticket', 'menus': (
                {'title': '系统日志', 'perm': self.get_model_perm(Log, 'view'), 'icon': 'fa fa-ticket',
                 'url': self.get_model_url(Log, 'changelist')},

            )},

        )


xadmin.site.register(CommAdminView, GlobalSetting)



# class ProductAdmin(object):
#     # list_display = ('name','status',)
#     # object_list_template = "xadmin/newproduct.html"
#     # add_form_template = 'xadmin/model_form.html'   # newproduct.html'
#     add_form_template = 'xadmin/newproduct.html'
#     form = ETHProductForm


class SiteUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
    style_fields = {'user_permissions': 'm2m_transfer'}
    model_icon = 'fa fa-user'
    relfield_style = 'fk-ajax'
    # list_display = ('name','status',)
    # object_list_template = "xadmin/newproduct.html"
    # add_form_template = 'xadmin/model_form.html'   # newproduct.html'
    # add_form_template = 'xadmin/newproduct.html'
    # form = ETHProductForm


class SiteGroupAdmin(GroupAdmin):
    pass


class CGroupAdmin(object):
    list_display = ('name',)
    ordering = ('name',)





class SitePermissionAdmin(object):
    pass



class DashboardModelAdmin(object):
    pass



xadmin.site.unregister(SiteUser)
xadmin.site.unregister(Permission)
xadmin.site.register(SitePermission, SitePermissionAdmin)
xadmin.site.unregister(Group)
xadmin.site.register(SiteUser, SiteUserAdmin)
xadmin.site.register(SiteGroup, SiteGroupAdmin)




