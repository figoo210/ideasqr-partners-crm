from django.urls import re_path

from .consumers import ChartConsumer, RealtimeDataConsumer

websocket_urlpatterns = [
    re_path(r"ws/get-teams-performance/", ChartConsumer.as_asgi()),
    re_path(r"ws/realtime-data/", RealtimeDataConsumer.as_asgi()),
]
