from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r"users", views.UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("countries", view=views.CountryListView.as_view()),
]
