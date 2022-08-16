from turtle import home
from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(home_list)
admin.site.register(device_type)
admin.site.register(device_data)
admin.site.register(added_device_list)
admin.site.register(category_detail)
admin.site.register(home_admin)
# admin.site.unregister(Group)
