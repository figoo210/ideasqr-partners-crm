# views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from crm_lead_core.custom_views import RoleBasedPermissionMixin
from .models import Product
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductCreateView(LoginRequiredMixin, RoleBasedPermissionMixin, CreateView):
    required_roles = ["Super Admin", "Admin"]
    model = Product
    form_class = ProductForm
    template_name = "products/add_product.html"
    success_url = "/products"


class ProductUpdateView(LoginRequiredMixin, RoleBasedPermissionMixin, UpdateView):
    required_roles = ["Super Admin", "Admin"]
    model = Product
    form_class = ProductForm
    template_name = "products/update_product.html"
    success_url = "/products"


class ProductListView(LoginRequiredMixin, RoleBasedPermissionMixin, ListView):
    required_roles = ["Super Admin", "Admin", "Team Leader"]
    model = Product
    template_name = "products/products.html"
    context_object_name = "products"
