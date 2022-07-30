from turtle import home
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(user_belong_home)
admin.site.register(home_list)
admin.site.register(device_type)
admin.site.register(device_data)
admin.site.register(added_device_list)
admin.site.register(alive_verification_code)
admin.site.register(category_detail)

