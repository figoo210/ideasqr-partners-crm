from datetime import datetime
from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.paginator import Paginator

from crm_lead_core.custom_views import (
    JsonableResponseMixin,
    RoleBasedPermissionMixin,
    role_required,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import CustomUser, Shift, get_all_users
from submissions.models import Submission

from .forms import CreateUserForm, ShiftForm, UpdateUserForm


class CustomLoginView(JsonableResponseMixin, LoginView):
    template_name = "accounts/login.html"
    next_page = "/employees"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # User is already logged in, so redirect to the specified next_page
            return redirect(self.next_page)

        return super().dispatch(request, *args, **kwargs)


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "accounts/change_password.html"
    success_url = "/account"


class AddEmployeeView(LoginRequiredMixin, RoleBasedPermissionMixin, CreateView):
    required_roles = ["Super Admin", "Admin"]
    model = CustomUser
    template_name = "accounts/add_employee.html"
    form_class = CreateUserForm
    success_url = "/employees"

    def form_valid(self, form):
        if not form.instance.team_leader:
            form.instance.team_leader = self.request.user
        if not form.instance.is_active:
            form.instance.is_active = True
        return super().form_valid(form)


class UpdateEmployeeView(LoginRequiredMixin, RoleBasedPermissionMixin, UpdateView):
    required_roles = ["Super Admin", "Admin"]
    model = CustomUser
    template_name = "accounts/update_employee.html"
    success_url = "/employees"
    form_class = UpdateUserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team_leader_username"] = CustomUser.objects.get(
            pk=self.kwargs["pk"]
        ).team_leader.username
        return context

    def form_valid(self, form):
        user_pk = self.kwargs["pk"]
        user = CustomUser.objects.get(pk=user_pk)
        new_password = form.cleaned_data["new_password"]
        user.set_password(new_password)  # This method hashes the password
        user.save()
        return super().form_valid(form)


class UpdateAccountView(LoginRequiredMixin, RoleBasedPermissionMixin, UpdateView):
    required_roles = ["Super Admin", "Admin", "Team Leader", "Employee"]
    model = CustomUser
    template_name = "accounts/account.html"
    success_url = "/account"
    form_class = UpdateUserForm

    def get_object(self, queryset=None):
        pk = self.request.user.id
        queryset = self.get_queryset()
        queryset = queryset.filter(pk=pk)
        obj = queryset.get()
        return obj


class ProfileView(LoginRequiredMixin, RoleBasedPermissionMixin, TemplateView):
    required_roles = ["Super Admin", "Admin", "Team Leader", "Employee"]
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["states"] = {
            "new_clients": Submission.objects.filter(date=datetime.today().date())
            .all()
            .count()
            or "-",
            "active_user": CustomUser.objects.filter(is_active=True).all().count()
            or "-",
            "inactive_user": CustomUser.objects.filter(is_active=False).all().count()
            or "-",
            "members": CustomUser.objects.all().count() or "-",
        }
        return context


class EmployeesView(LoginRequiredMixin, RoleBasedPermissionMixin, TemplateView):
    required_roles = ["Super Admin", "Admin", "Team Leader"]
    template_name = "accounts/employees.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_data = get_all_users(self.request.user)
        paginator = Paginator(all_data, per_page=100)
        page_number = (
            int(self.request.GET.get("page")) if "page" in self.request.GET else 1
        )
        page_obj = paginator.get_page(page_number)
        context["users"] = page_obj
        context["page_obj"] = page_obj
        return context


@role_required(["Super Admin", "Admin"])
def delete_user(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    user.delete()
    return redirect("/employees")  # Redirect to the user list page


@role_required(["Super Admin", "Admin"])
def activate_user(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    user.is_active = True
    user.save()
    return redirect("/employees")  # Redirect to the user list page


@role_required(["Super Admin", "Admin", "Team Leader", "Employee"])
def deactivate_user(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    user.is_active = False
    user.save()
    return redirect("/employees")  # Redirect to the user list page


def logoutUser(request):
    logout(request=request)
    return redirect("/login")


class ShiftCreateView(LoginRequiredMixin, RoleBasedPermissionMixin, View):
    required_roles = ["Super Admin", "Admin"]
    template_name = "accounts/shift.html"

    def get(self, request):
        shift = Shift.objects.filter(pk=1).first()
        if shift:
            form = ShiftForm(instance=shift)
        else:
            form = ShiftForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        shift = Shift.objects.filter(pk=1).first()
        form = ShiftForm(request.POST)
        if form.is_valid() and not shift:
            form.save()
            return redirect("/shift")  # Redirect to a view displaying all shifts
        else:
            shift.start_time = form.data.get("start_time")
            shift.end_time = form.data.get("end_time")
            shift.save()
        return render(request, self.template_name, {"form": form})


class TeamLeaderSearchView(View):
    def get(self, request, *args, **kwargs):
        search_term = request.GET.get("search_term", "")
        if search_term and len(search_term) > 0:
            users = self.get_matching_users(search_term)
            user_data = list(users.values("id", "username"))
            return JsonResponse({"team_leaders": user_data})
        else:
            return JsonResponse(
                {
                    "team_leaders": list(
                        CustomUser.objects.filter(team_leader=self.request.user).values(
                            "id", "username"
                        )
                    )
                }
            )

    def get_matching_users(self, search_term):
        # Customize this method based on your User model and search criteria
        return CustomUser.objects.filter(
            role="Team Leader", username__icontains=search_term
        ).all()


class EmployeeSearchView(View):
    def get(self, request, *args, **kwargs):
        search_term = request.GET.get("search_term", "")
        users = get_all_users(self.request.user)
        if search_term and len(search_term) > 0:
            user_data = list(
                users.filter(username__icontains=search_term).values("id", "username")
            )
            return JsonResponse({"employees": user_data})
        else:
            user_data = list(users.values("id", "username"))
            return JsonResponse({"employees": user_data})
