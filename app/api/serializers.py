from rest_framework import serializers
from api.models import *


class userSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
class user_belong_homeSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_belong_home
        fields = ('user_id', 'home_id')


class home_listSerializer(serializers.ModelSerializer):

    class Meta:
        model = home_list
        fields = ('home_address', 'home_owner')


class added_device_listSerializer(serializers.ModelSerializer):

    class Meta:
        model = added_device_list
        fields = ('added_time', 'device_type_id', 'home_id')


class device_typeSerializer(serializers.ModelSerializer):

    class Meta:
        model = device_type
        fields = ('device_type_name', 'device_type_description', 'category')


class alive_verification_codeSerializer(serializers.ModelSerializer):

    class Meta:
        model = alive_verification_code
        fields = ('type', 'verification_code', 'address')


class categorySerializer(serializers.ModelSerializer):

    class Meta:
        model = category_detail
        fields = ('category_name', 'category_description')


class device_dataSerializer(serializers.ModelSerializer):

    class Meta:
        model = device_data
        fields = ('device_id', 'device_type', 'data_value', 'data_time')

class mode_key_dataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = mode_key_data
        fields = ('mode_key_data_id', 'home_id', 'tplink_switch_mode_key','mode_key_time')
