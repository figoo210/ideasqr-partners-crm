from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from reports.services import get_user_timezone_info


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["timezone"] = get_user_timezone_info()
        return context
