from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/comments-server/', consumers.CommentsConsumer.as_asgi())
]