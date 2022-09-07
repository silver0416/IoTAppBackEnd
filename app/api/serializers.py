from urllib import request
from rest_framework import serializers
from api.models import *
from hashid_field.rest import HashidSerializerCharField
from rest_framework.decorators import authentication_classes, permission_classes


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class homeAdminSerializer(serializers.ModelSerializer):
    home = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(source_field="api.home_list.home_id"),
        read_only=True,
    )

    class Meta:
        model = home_admin
        fields = "__all__"


class homeSerializer(serializers.ModelSerializer):
    home_id = HashidSerializerCharField(
        source_field="api.home_list.home_id", read_only=True
    )

    class Meta:
        model = home_list
        fields = "__all__"


class device_listSerializer(serializers.ModelSerializer):
    home = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(source_field="api.home_list.home_id"),
        queryset=home_list.objects.all(),
    )
    class Meta:
        model = device_list
        fields = "__all__"

class device_dataSerializer(serializers.ModelSerializer):
    home = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(source_field="api.home_list.home_id"),
        queryset=home_list.objects.all(),
    )
    class Meta:
        model = device_data
        fields = "__all__"


class mode_key_dataSerializer(serializers.ModelSerializer):
    home_id = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(source_field="api.home_list.home_id"),
        queryset=home_list.objects.all(),
    )

    class Meta:
        model = mode_key_data
        fields = (
            "mode_key_data_id",
            "mode_key_name",
            "home_id",
            "tplink_switch_mode_key",
            "ac_temperature",
            "ac_switch",
            "fan_level",
            "fan_switch",
            "mode_key_time",
        )


class chat_room_data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = chat_room_data
        fields = "__all__"


class chat_room_serializer(serializers.ModelSerializer):
    class Meta:
        model = chat_room
        fields = "__all__"
