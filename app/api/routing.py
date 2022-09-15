from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/device/(?P<home_name>\w+)/$', consumers.DeviceConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
