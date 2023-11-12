import fnmatch
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, CreateView, UpdateView, ListView


from datetime import datetime
from accounts.models import CustomUser
from crm_lead_core.custom_views import RoleBasedPermissionMixin, role_required
from feedbacks.models import Feedback

from products.models import Product, SubmissionProducts
from queues.models import UserQueue

from .forms import AddSubmissionForm, StatusForm
from .models import Status, Submission, get_submissions_based_on_role


class SubmissionsView(RoleBasedPermissionMixin, TemplateView):
    required_roles = ["Super Admin", "Admin", "Team Leader", "Employee"]
    template_name = "submissions/submissions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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

        context["submissions"] = get_submissions_based_on_role(
            user=self.request.user,
            user_team_leaders=user_team_leaders,
            user_team_leaders_employees=user_team_leaders_employees,
        )
        context["all_status"] = Status.objects.all()
        context["feedbacks"] = Feedback.objects.all()
        return context


class AddSubmissionView(RoleBasedPermissionMixin, CreateView):
    required_roles = ["Super Admin", "Admin", "Team Leader", "Employee"]
    template_name = "submissions/add_submission.html"
    model = Submission
    form_class = AddSubmissionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        timenow = datetime.now().strftime("%d/%m/%Y %I:%M %p")
        context["timestamp"] = timenow
        context[
            "employee"
        ] = f"{self.request.user.first_name} {self.request.user.last_name}"
        context["team_leader"] = (
            f"{self.request.user.team_leader.first_name} {self.request.user.team_leader.last_name}"
            or "No Team Manager"
        )
        context["status"] = Status.objects.all()
        context["products"] = Product.objects.all()

        return context

    def post(self, request, **kwargs):
        if request.POST:
            data = request.POST
            new_submission = Submission(
                medical_id=data["medical_id"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                middle_initial=data["middle_initial"]
                if "middle_initial" in data
                else None,
                phone=data["phone"],
                birth_date=f'{data["birth_date_year"]}-{data["birth_date_month"]}-{data["birth_date_day"]}',
                address=data["address"],
                city=data["city"],
                state=data["state"],
                zip_code=data["zip_code"],
                comment=data["comment"],
                # status=data["status"],
                user_queue=UserQueue.objects.filter(user=self.request.user).last(),
            )
            new_submission.save()

            # Submission Products
            wildcard_checkbox = "checkbox-*"
            matching_keys = [
                key for key in data if fnmatch.fnmatch(key, wildcard_checkbox)
            ]
            for k in matching_keys:
                product = Product.objects.get(pk=data[f"count-{k.split('-')[1]}"])
                new_submission_product = SubmissionProducts(
                    count=int(data[f"count-{k.split('-')[1]}"])
                    if f"count-{k.split('-')[1]}" in data
                    else 1,
                    submission=new_submission,
                    product=product,
                )
                new_submission_product.save()
        return redirect("/submissions")


class UpdateSubmissionView(RoleBasedPermissionMixin, UpdateView):
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
            new_submission = Submission(
                medical_id=data["medical_id"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                middle_initial=data["middle_initial"]
                if "middle_initial" in data
                else None,
                phone=data["phone"],
                birth_date=f'{data["birth_date_year"]}-{data["birth_date_month"]}-{data["birth_date_day"]}',
                address=data["address"],
                city=data["city"],
                state=data["state"],
                zip_code=data["zip_code"],
                comment=data["comment"],
                # status=data["status"],
                user_queue=UserQueue.objects.filter(user=self.request.user).last(),
            )
            new_submission.save()

            # Submission Products
            wildcard_checkbox = "checkbox-*"
            matching_keys = [
                key for key in data if fnmatch.fnmatch(key, wildcard_checkbox)
            ]
            for k in matching_keys:
                product = Product.objects.get(pk=data[f"count-{k.split('-')[1]}"])
                new_submission_product = SubmissionProducts(
                    count=int(data[f"count-{k.split('-')[1]}"])
                    if f"count-{k.split('-')[1]}" in data
                    else 1,
                    submission=new_submission,
                    product=product,
                )
                new_submission_product.save()
        return redirect("/submissions")


@role_required(["Super Admin", "Admin", "Team Leader"])
def update_submission_status(request, *args, **kwargs):
    """Update the status of a submission."""
    if request.method == "GET":
        id = kwargs.get("id")
        status = Status.objects.get(name=kwargs.get("status"))
        submission = get_object_or_404(Submission, pk=id)
        submission.status = status
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


class StatusCreateView(RoleBasedPermissionMixin, CreateView):
    required_roles = ["Super Admin", "Admin"]
    model = Status
    form_class = StatusForm
    template_name = "status/add_status.html"
    success_url = "/status"


class StatusUpdateView(RoleBasedPermissionMixin, UpdateView):
    required_roles = ["Super Admin", "Admin"]
    model = Status
    form_class = StatusForm
    template_name = "status/update_status.html"
    success_url = "/status"


class StatusListView(RoleBasedPermissionMixin, ListView):
    required_roles = ["Super Admin", "Admin", "Team Leader"]
    model = Status
    template_name = "status/status.html"
    context_object_name = "status"
