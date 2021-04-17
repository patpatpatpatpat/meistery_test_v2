from . import views

from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r"sales", views.SaleViewSet, basename="sales")

urlpatterns = [
    path("", include(router.urls)),
    path("sale_statistics/", views.SaleStatisticsView.as_view()),
]
