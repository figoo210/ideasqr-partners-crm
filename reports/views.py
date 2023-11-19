from django.shortcuts import redirect, render, HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q

from accounts.models import CustomUser

from reports.services import get_user_timezone_info

from dotenv import load_dotenv
import os

load_dotenv()


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["DASHBOARD_WEBSOCKET_URL"] = os.environ.get("DASHBOARD_WEBSOCKET_URL")
        context["REALTIME_WEBSOCKET_URL"] = os.environ.get("REALTIME_WEBSOCKET_URL")

        context["timezone"] = get_user_timezone_info()
        context["users_count"] = CustomUser.objects.filter(
            is_superuser=False, is_staff=False
        ).count()

        nine_hours_ago = timezone.now() - timezone.timedelta(hours=9)
        context["active_users_count"] = CustomUser.objects.filter(
            is_superuser=False, is_staff=False, last_login__gte=nine_hours_ago
        ).count()

        context["inactive_users_count"] = CustomUser.objects.filter(
            Q(is_superuser=False, is_staff=False, last_login__lt=nine_hours_ago)
            | Q(is_superuser=False, is_staff=False, last_login__isnull=True)
        ).count()

        return context


class TokenScreenView(TemplateView):
    template_name = "reports/realtime_data.html"

    def dispatch(self, request, *args, **kwargs):
        token = self.request.GET.get("token")
        if not token or token != os.environ.get("SCREEN_TOKEN"):
            return HttpResponseRedirect("/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["REALTIME_WEBSOCKET_URL"] = os.environ.get("REALTIME_WEBSOCKET_URL")
        return context
