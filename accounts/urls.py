from django.urls import path
from .views import (
    CustomLoginView,
    AddEmployeeView,
    EmployeesView,
    ShiftCreateView,
    UpdateEmployeeView,
    UpdateAccountView,
    ProfileView,
    delete_user,
    activate_user,
    deactivate_user,
    logoutUser,
)

urlpatterns = [
    path("login", CustomLoginView.as_view(), name="Login"),
    path("logout", logoutUser, name="Logout"),
    path("add-employee", AddEmployeeView.as_view(), name="add_employee"),
    path("employees", EmployeesView.as_view(), name="employees"),
    path("employees/edit/<str:pk>/", UpdateEmployeeView.as_view(), name="update_user"),
    path("account", UpdateAccountView.as_view(), name="account"),
    path("profile", ProfileView.as_view(), name="profile"),
    path("employees/<str:user_id>/delete/", delete_user, name="delete_user"),
    path("employees/<str:user_id>/activate/", activate_user, name="activate_user"),
    path(
        "employees/<str:user_id>/deactivate/", deactivate_user, name="deactivate_user"
    ),
    # SHIFT
    path("shift", ShiftCreateView.as_view(), name="shift_create"),
]
