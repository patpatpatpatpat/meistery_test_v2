"""meistery_trial_assignment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path, include
from . import views
from users.views import CreateUserView, EditUserView
from sales.views import ClearUserSalesView, AddUserSalesView, ProductInfoInputPage


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("meistery_trial_assignment.api.urls")),

    path("create_user/", CreateUserView.as_view(), name="create_user"),
    path("edit_user/<pk>/", EditUserView.as_view(), name="edit_user"),
    path("edit_user/<pk>/clear_sales/", ClearUserSalesView.as_view(), name="clear_sales_for_user"),
    path("edit_user/<pk>/add_sales/", AddUserSalesView.as_view(), name="add_sales_for_user"),
    path("product_info_input/", ProductInfoInputPage.as_view(), name="product_info_input"),

    # DRF
    path("api-auth/", include("rest_framework.urls")),
    # SPA view
    re_path(r"^.*$", views.react, name="home"),
]
