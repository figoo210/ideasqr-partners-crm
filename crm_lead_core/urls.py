"""crm_lead_core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


def favicon(request):
    return HttpResponse(200)


def test(request):
    return render(request, "test/index.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("favicon.ico", favicon),
    path("test", test),
    path("", include("accounts.urls")),
    path("", include("reports.urls")),
    path("", include("submissions.urls")),
    path("", include("queues.urls")),
    path("", include("products.urls")),
    path("", include("tasks.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
