from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, ListView
from django.urls import reverse_lazy
from django.db.models import OuterRef, Subquery
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from accounts.models import CustomUser, get_all_users
from crm_lead_core.custom_views import RoleBasedPermissionMixin, role_required

from .forms import QueueForm
from .models import Queue, UserQueue


class QueueCreateView(LoginRequiredMixin, RoleBasedPermissionMixin, CreateView):
    required_roles = ["Super Admin", "Admin"]
    model = Queue
    form_class = QueueForm
    template_name = "queues/queue_form.html"
    success_url = "/queues"


class QueueUpdateView(LoginRequiredMixin, RoleBasedPermissionMixin, UpdateView):
    required_roles = ["Super Admin", "Admin"]
    model = Queue
    form_class = QueueForm
    template_name = "queues/queue_form.html"
    success_url = "/queues"


class QueueListView(LoginRequiredMixin, RoleBasedPermissionMixin, ListView):
    required_roles = ["Super Admin", "Admin", "Team Leader"]
    model = Queue
    template_name = "queues/queues.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Subquery to get the latest created_at for each queue
        latest_created_subquery = (
            UserQueue.objects.filter(queue_id=OuterRef("queue_id"))
            .order_by("-created_at")
            .values("created_at")[:1]
        )
        # Query to get the whole rows for the latest created_at timestamps
        latest_records = UserQueue.objects.filter(
            created_at=Subquery(latest_created_subquery)
        )

        all_data = Queue.objects.all()
        paginator = Paginator(all_data, per_page=100)
        page_number = (
            int(self.request.GET.get("page")) if "page" in self.request.GET else 1
        )
        page_obj = paginator.get_page(page_number)

        context["page_obj"] = page_obj
        context["users"] = get_all_users(self.request.user)
        context["queues"] = page_obj
        context["queues_users"] = latest_records

        return context


@role_required(["Super Admin", "Admin"])
def delete_queue(request, queue_id):
    queue = Queue.objects.get(pk=queue_id)
    queue.delete()
    return redirect("/queues")


@role_required(["Super Admin", "Admin", "Team Leader"])
def update_queue_user(request):
    if request.method == "POST":
        user = CustomUser.objects.filter(username=request.POST["username"]).first()
        queue = Queue.objects.get(pk=request.POST["queue_id"])
        if user:
            new_user_queue = UserQueue(
                user=user,
                queue=queue,
            )
            new_user_queue.save()

    return redirect("/queues")


@role_required(["Super Admin", "Admin", "Team Leader"])
def update_queue_website(request):
    if request.method == "POST":
        if "website" in request.POST and request.POST["website"]:
            website = request.POST["website"]
            user_queue = request.POST["user_queue"]
            uq = UserQueue.objects.get(pk=int(user_queue))
            uq.website = website
            uq.save()
    return redirect("/queues")
