from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/<int:room_id>/', consumers.ChatConsumer.as_asgi()),
    path('ws/ghep/<int:kieu_ghep>/', consumers.GhepConsumer.as_asgi()),
]