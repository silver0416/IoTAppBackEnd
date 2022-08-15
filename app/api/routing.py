from django.urls import re_path,path
from .import consumers

websocket_urlpatterns = [
    re_path(r'ws/dht11/(?P<home_name>\w+)/$', consumers.IotConsumer.as_asgi()),
    re_path(r'ws/mq7/(?P<home_name>\w+)/$', consumers.IotConsumer.as_asgi()),
    re_path(r'ws/sr501/(?P<home_name>\w+)/$', consumers.IotConsumer.as_asgi()),
]