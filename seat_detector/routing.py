from django.urls import re_path
from seat_detector.consumer import SocketConsumer

# URLs for websockects connection
websocket_urlpatterns = [
    re_path('ws/data-stream/', SocketConsumer.as_asgi())
]