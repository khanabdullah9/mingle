from django.urls import re_path,path
# from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$',consumers.ChatRoomConsumer.as_asgi()),
]