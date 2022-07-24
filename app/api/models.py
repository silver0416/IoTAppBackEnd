# pylint: disable=missing-module-docstring
from unicodedata import category
from xml.dom.minidom import Identified
from django.db import models


# Create your models here.

class user_info(models.Model):
    user_id = models.AutoField(blank=False,null=False,primary_key=True,auto_created=True)
    user_name = models.TextField(blank=False,null=False,default=' ')
    user_password = models.TextField(blank=False,null=False,default=' ')
    user_nickname = models.CharField(max_length = 30,blank=True,null=True )
    user_phone = models.CharField(max_length = 30,blank=True,null=True )
    user_email = models.EmailField(max_length = 30,blank=False,null=True )


class user_belong_home(models.Model):
    user_belong_home = models.AutoField(blank=False,null=False,primary_key=True,auto_created=True)
    user_id = models.ForeignKey(user_info, related_name='belong_home',on_delete=models.CASCADE)
    home_id = models.ForeignKey('home_list', related_name='belong_user',on_delete=models.CASCADE)

class home_list(models.Model):
    home_id = models.AutoField(blank=False,null=False,primary_key=True,auto_created=True)
    home_address = models.CharField(max_length = 30,blank=False,null=False,default=' ')
    home_owner = models.ForeignKey(user_info, on_delete=models.CASCADE)



class device_type(models.Model):
    device_type_id = models.AutoField(blank=False,null=False,primary_key=True,auto_created=True)
    device_type_name = models.CharField(max_length = 30,blank=False,null=False)
    device_type_description = models.CharField(max_length = 30,blank=True,null=False)
    category = models.ForeignKey('category_detail', on_delete=models.CASCADE)

class added_device_list(models.Model):
    added_device_id = models.AutoField(blank=False,null=False,primary_key=True,auto_created=True)
    added_time = models.DateTimeField(auto_now_add=True)
    home_id = models.ForeignKey(home_list, on_delete=models.CASCADE)
    device_type_id = models.ForeignKey(device_type, on_delete=models.CASCADE)

class alive_verification_code(models.Model):
    alive_verification_code_id = models.AutoField(blank=False,null=False,primary_key=True,auto_created=True)
    type = models.CharField(max_length = 30,blank=False,null=False)
    verification_code = models.IntegerField(blank=False,null=False)
    start_time = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length = 50,blank=False,null=False)

class category_detail(models.Model):
    category_id = models.AutoField(blank=False,null=False,primary_key=True,auto_created=True)
    category_name = models.CharField(max_length = 30,blank=False,null=False)
    category_description = models.CharField(max_length = 30,blank=True,null=False)
    
class device_data(models.Model):
    device_data_id = models.AutoField(blank=False,null=False,primary_key=True,auto_created=True)
    device_id = models.ForeignKey(added_device_list, on_delete=models.CASCADE)
    device_type = models.ForeignKey(device_type, on_delete=models.CASCADE)
    data_value = models.CharField(max_length = 30,blank=False,null=False)
    data_time = models.DateTimeField(auto_now_add=True)
    

