from django.urls import path

from reports.consumers import ChartConsumer
from .views import DashboardView, TokenScreenView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("realtime-data", TokenScreenView.as_view(), name="realtime_data"),
    path("ws/get-teams-performance/", ChartConsumer.as_asgi()),
]
