# -*- coding: utf-8 -*-
from django.urls import include, path

from .users.views import CustomAuthToken, LogoutView

urlpatterns = [
    path("login", CustomAuthToken.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("", include("meistery_trial_assignment.api.users.urls")),
    path("", include("meistery_trial_assignment.api.sales.urls")),
]
