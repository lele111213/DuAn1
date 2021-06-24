from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/<str:room_id>/', consumers.ChatConsumer.as_asgi()),
    path('ws/<int:kieu_ghep>/', consumers.GhepConsumer.as_asgi()),
]