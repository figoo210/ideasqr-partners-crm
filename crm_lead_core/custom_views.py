from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render


def role_required(required_roles):
    def decorator(view_func):
        @login_required
        @user_passes_test(lambda user: user.role in required_roles)
        def wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator


# @role_required(["Super Admin", "Admin"])
# def my_protected_function_view(request):


class RoleBasedPermissionMixin(LoginRequiredMixin):
    required_roles = []

    def check_user_role(self, user):
        return user.role in self.required_roles

    def dispatch(self, request, *args, **kwargs):
        if not self.check_user_role(request.user):
            return render(request, "403.html", status=403)
        return super().dispatch(request, *args, **kwargs)


class JsonableResponseMixin:
    """
    Mixin to add JSON support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        print("Invalid Request: ", form.errors)
        if self.request.accepts("text/html"):
            return response
        else:
            return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        print("Valid Request")
        response = super().form_valid(form)
        if self.request.accepts("text/html"):
            return response
        else:
            data = {
                "pk": self.object.pk,
            }
            return JsonResponse(data)
