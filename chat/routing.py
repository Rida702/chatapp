from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi(), name='one2one_chat'),
    path('ws/chat/group/<str:group_name>/', consumers.ChatConsumer.as_asgi(), name='group_chat'),
]
