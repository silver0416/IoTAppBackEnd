from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/dht11/(?P<home_name>\w+)/$', consumers.IotConsumer.as_asgi()),
    # re_path(r'ws/mq7/(?P<home_name>\w+)/$', consumers.IotConsumer.as_asgi()),
    # re_path(r'ws/sr501/(?P<home_name>\w+)/$', consumers.IotConsumer.as_asgi()),
    re_path(r"ws/message/(?P<user_name>\w+)/$", consumers.MessageConsumer.as_asgi()),
    re_path(r"ws/(?P<home_name>\w+)/$", consumers.StripConsumer.as_asgi()),
    re_path(r"ws/strip/(?P<home_name>\w+)/$", consumers.StripConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
