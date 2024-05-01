import fnmatch
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from django.core.paginator import Paginator
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime
from accounts.models import CustomUser
from crm_lead_core.custom_views import RoleBasedPermissionMixin, role_required
from feedbacks.models import Feedback

from products.models import Product, SubmissionProducts
from queues.models import UserQueue
from reports.realtime_data import send_realtime_data

from .forms import AddSubmissionForm, CloserForm, LeaderStatusForm, StatusForm
from .models import (
    Closers,
    LeaderStatus,
    Status,
    Submission,
    get_submissions_based_on_role,
)


class SubmissionsView(LoginRequiredMixin, RoleBasedPermissionMixin, TemplateView):
    required_roles = ["Super Admin", "Admin", "Team Leader", "Employee"]
    template_name = "submissions/submissions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("query")

        user_team_leaders = CustomUser.objects.filter(
            team_leader=self.request.user
        ).all()

        user_team_leaders_employees = CustomUser.objects.none()
        if user_team_leaders and len(user_team_leaders) > 0:
            for utl in user_team_leaders:
                team_leader_employees = CustomUser.objects.filter(team_leader=utl).all()
                if team_leader_employees and len(team_leader_employees) > 0:
                    user_team_leaders_employees |= team_leader_employees
        else:
            user_team_leaders_employees = CustomUser.objects.filter(
                team_leader=self.request.user
            ).all()

        all_data = get_submissions_based_on_role(
            user=self.request.user,
            user_team_leaders=user_team_leaders,
            user_team_leaders_employees=user_team_leaders_employees,
        )

        if search_query:
            all_data = all_data.filter(
                Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
                | Q(phone__icontains=search_query)
            )

        paginator = Paginator(all_data, per_page=100)
        page_number = (
            int(self.request.GET.get("page")) if "page" in self.request.GET else 1
        )
        page_obj = paginator.get_page(page_number)

        context["page_obj"] = page_obj
        context["submissions"] = page_obj
        context["all_status"] = LeaderStatus.objects.all()
        context["feedbacks"] = Feedback.objects.all()
        return context


class AddSubmissionView(LoginRequiredMixin, RoleBasedPermissionMixin, CreateView):
    required_roles = ["Super Admin", "Admin", "Team Leader", "Employee"]
    template_name = "submissions/add_submission.html"
    model = Submission
    form_class = AddSubmissionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        timenow = datetime.now().strftime("%d/%m/%Y %I:%M %p")
        context["timestamp"] = timenow
        context["employee"] = (
            f"{self.request.user.first_name} {self.request.user.last_name}"
        )
        context["team_leader"] = (
            f"{self.request.user.team_leader.first_name if self.request.user.team_leader else self.request.user.first_name} {self.request.user.team_leader.last_name if self.request.user.team_leader else self.request.user.last_name}"
            or "No Team Manager"
        )
        context["status"] = Status.objects.all()
        context["closers"] = Closers.objects.all()
        context["products"] = Product.objects.all()
        current_year = datetime.now().year
        context["years"] = range(1900, current_year + 1)

        return context

    def post(self, request, **kwargs):
        if request.POST:
            data = request.POST
            new_submission = Submission(
                medical_id=data["medical_id"],
                pos_type=data["pos_type"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                middle_initial=(
                    data["middle_initial"] if "middle_initial" in data else None
                ),
                phone=data["phone"],
                phone2=data["phone2"],
                birth_date=f'{data["birth_date_year"]}-{data["birth_date_month"]}-{data["birth_date_day"]}',
                address=data["address"],
                city=data["city"],
                state=data["state"],
                insurance_type=(
                    data["insurance_type"] if "insurance_type" in data else "No Info"
                ),
                zip_code=data["zip_code"],
                comment=data["comment"],
                status=(
                    Status.objects.get(name=data["status"])
                    if "status" in data
                    else None
                ),
                closer=(
                    Closers.objects.get(name=data["closer"])
                    if "closer" in data
                    else None
                ),
                user_queue=UserQueue.objects.filter(user=self.request.user).last(),
            )
            new_submission.save(request=request)

            # Submission Products
            wildcard_checkbox = "checkbox-*"
            matching_keys = [
                key for key in data if fnmatch.fnmatch(key, wildcard_checkbox)
            ]
            for k in matching_keys:
                product = Product.objects.get(pk=k.split("-")[1])
                new_submission_product = SubmissionProducts(
                    count=(
                        int(data[f"count-{k.split('-')[1]}"])
                        if f"count-{k.split('-')[1]}" in data
                        else 1
                    ),
                    submission=new_submission,
                    product=product,
                )
                new_submission_product.save()
        send_realtime_data("get data")
        return redirect("/submissions")


class UpdateSubmissionView(LoginRequiredMixin, RoleBasedPermissionMixin, UpdateView):
    required_roles = ["Super Admin", "Admin", "Team Leader"]
    template_name = "submissions/update_submission.html"
    model = Submission
    form_class = AddSubmissionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["submission"] = Submission.objects.get(pk=self.kwargs["pk"])
        context["submission_products"] = SubmissionProducts.objects.filter(
            submission_id=self.kwargs["pk"]
        ).all()
        context["status"] = Status.objects.all()
        context["products"] = Product.objects.all()

        return context

    def post(self, request, **kwargs):
        if request.POST:
            data = request.POST
            submission = Submission.objects.get(pk=self.kwargs["pk"])
            submission.medical_id = data["medical_id"]
            submission.first_name = data["first_name"]
            submission.last_name = data["last_name"]
            submission.middle_initial = (
                data["middle_initial"] if "middle_initial" in data else None
            )
            submission.phone = data["phone"]
            submission.address = data["address"]
            submission.city = data["city"]
            submission.state = data["state"]
            submission.zip_code = data["zip_code"]
            submission.comment = data["comment"]
            submission.status = Status.objects.get(name=data["status"])
            submission.save()

        return redirect("/submissions")


@role_required(["Super Admin", "Admin", "Team Leader"])
def update_submission_status(request, *args, **kwargs):
    """Update the status of a submission."""
    if request.method == "GET":
        id = kwargs.get("id")
        status = LeaderStatus.objects.get(name=kwargs.get("status"))
        submission = get_object_or_404(Submission, pk=id)
        submission.leader_status = status
        submission.save()
        return redirect("/submissions")


@role_required(["Super Admin", "Admin", "Team Leader", "Employee"])
def update_submission_comment(request, *args, **kwargs):
    """Update the comment of a submission."""
    if request.method == "POST":
        data = request.POST
        submission = Submission.objects.get(pk=int(data["submission_id"]))
        submission.comment = data["comment"]
        submission.save()
        return redirect("/submissions")


@role_required(["Super Admin", "Admin", "Team Leader"])
def add_submission_feedback(request, *args, **kwargs):
    """Update the comment of a submission."""
    if request.method == "POST":
        data = request.POST
        submission = Submission.objects.get(pk=int(data["submission_id"]))
        feedback = Feedback(
            content=data["feedback"], user=request.user, submission=submission
        )
        feedback.save()
        return redirect("/submissions")


class StatusCreateView(LoginRequiredMixin, RoleBasedPermissionMixin, CreateView):
    required_roles = ["Super Admin", "Admin"]
    model = Status
    form_class = StatusForm
    template_name = "status/add_status.html"
    success_url = "/status"


class StatusUpdateView(LoginRequiredMixin, RoleBasedPermissionMixin, UpdateView):
    required_roles = ["Super Admin", "Admin"]
    model = Status
    form_class = StatusForm
    template_name = "status/update_status.html"
    success_url = "/status"


class StatusListView(LoginRequiredMixin, RoleBasedPermissionMixin, ListView):
    required_roles = ["Super Admin", "Admin", "Team Leader"]
    model = Status
    template_name = "status/status.html"
    context_object_name = "status"


class LeaderStatusCreateView(LoginRequiredMixin, RoleBasedPermissionMixin, CreateView):
    required_roles = ["Super Admin", "Admin"]
    model = LeaderStatus
    form_class = LeaderStatusForm
    template_name = "status/add_leaderstatus.html"
    success_url = "/leaderstatus"


class LeaderStatusUpdateView(LoginRequiredMixin, RoleBasedPermissionMixin, UpdateView):
    required_roles = ["Super Admin", "Admin"]
    model = LeaderStatus
    form_class = LeaderStatusForm
    template_name = "status/update_leaderstatus.html"
    success_url = "/leaderstatus"


class LeaderStatusListView(LoginRequiredMixin, RoleBasedPermissionMixin, ListView):
    required_roles = ["Super Admin", "Admin", "Team Leader"]
    model = LeaderStatus
    template_name = "status/leaderstatus.html"
    context_object_name = "leaderstatus"


class ClosersCreateView(LoginRequiredMixin, RoleBasedPermissionMixin, CreateView):
    required_roles = ["Super Admin", "Admin"]
    model = Closers
    form_class = CloserForm
    template_name = "status/add_closers.html"
    success_url = "/closers"


class ClosersUpdateView(LoginRequiredMixin, RoleBasedPermissionMixin, UpdateView):
    required_roles = ["Super Admin", "Admin"]
    model = Closers
    form_class = CloserForm
    template_name = "status/update_closers.html"
    success_url = "/closers"


class ClosersListView(LoginRequiredMixin, RoleBasedPermissionMixin, ListView):
    required_roles = ["Super Admin", "Admin", "Team Leader"]
    model = Closers
    template_name = "status/closers.html"
    context_object_name = "closers"


@role_required(["Super Admin"])
def delete_status(request, status_name):
    status = Status.objects.get(pk=status_name)
    status.delete()
    return redirect("/status")


@role_required(["Super Admin"])
def delete_leaderstatus(request, status_name):
    status = LeaderStatus.objects.get(pk=status_name)
    status.delete()
    return redirect("/leaderstatus")


@role_required(["Super Admin"])
def delete_closer(request, status_name):
    status = Closers.objects.get(pk=status_name)
    status.delete()
    return redirect("/closers")
