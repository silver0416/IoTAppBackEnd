from turtle import home
from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *
# Register your models here.
admin.site.site_header = "IoT 後臺管理"
admin.site.site_title = "Your Admin Portal"
admin.site.index_title = "後臺服務"
admin.site.register(User)
# admin.site.register(home_list)
admin.site.register(device_type)
admin.site.register(device_data)
admin.site.register(added_device_list)
admin.site.register(category_detail)
# admin.site.register(home_admin)
# admin.site.unregister(Group)
@admin.register(home_list)
class homeInstanceAdmin(admin.ModelAdmin):
    list_display = ('display_id','display_home',"display_user")

    def display_id(self, obj):
        return obj.home_id
    display_id.short_description = "家庭編號"
    
    def display_user(self,obj):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ", ".join(user.username for user in obj.user.all()[:3])
    display_user.short_description = "家庭成員"

    def display_home(self, obj):
        return obj.home_name
    display_home.short_description = "家庭名稱"

@admin.register(home_admin)
class homeAdminInstanceAdmin(admin.ModelAdmin):
    list_display = ('id','home',"admin")