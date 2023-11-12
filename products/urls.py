# urls.py
from django.urls import path
from .views import (
    ProductCreateView,
    ProductUpdateView,
    ProductListView,
)

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/create", ProductCreateView.as_view(), name="product_create"),
    path(
        "products/<int:pk>/update", ProductUpdateView.as_view(), name="product_update"
    ),
    # path(
    #     "products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"
    # ),
]
