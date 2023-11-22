# views.py
from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
)
from .models import Task
from .forms import TaskForm
from crm_lead_core.custom_views import RoleBasedPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class TaskListView(LoginRequiredMixin, RoleBasedPermissionMixin, ListView):
    required_roles = ["Super Admin", "Admin", "Team Leader", "Employee"]
    model = Task
    template_name = "tasks/tasks.html"
    context_object_name = "tasks"


class TaskCreateView(LoginRequiredMixin, RoleBasedPermissionMixin, CreateView):
    required_roles = ["Super Admin", "Admin", "Team Leader", "Employee"]
    model = Task
    form_class = TaskForm
    template_name = "tasks/add_task.html"
    success_url = "/tasks"


class TaskUpdateView(LoginRequiredMixin, RoleBasedPermissionMixin, UpdateView):
    required_roles = ["Super Admin", "Admin", "Team Leader", "Employee"]
    model = Task
    form_class = TaskForm
    template_name = "tasks/add_task.html"
    success_url = "/tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = Task.objects.get(pk=self.kwargs["pk"]).to_user.username
        return context



def update_task_state(request, *args, **kwargs):
    task = Task.objects.get(pk=kwargs.get("id"))
    state = kwargs.get("state")
    task.state = state
    task.save()
    return redirect("/tasks")


def delete_task(request, *args, **kwargs):
    task = Task.objects.get(pk=kwargs.get("id"))
    task.delete()
    return redirect("/tasks")
