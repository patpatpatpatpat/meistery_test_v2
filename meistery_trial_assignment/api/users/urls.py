from . import views

from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),

     # TODO: rename url to countries?
    path('country_data', view=views.CountryListView.as_view()),
]