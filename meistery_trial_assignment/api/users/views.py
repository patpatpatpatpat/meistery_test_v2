from rest_framework import status
from django.shortcuts import render

from rest_framework import viewsets, mixins
from users.models import User, Country
from .serializers import UserSerializer, CountrySerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView


class UserViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CountryListView(ListAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class LogoutView(APIView):  # TODO: use login_required?
    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class CustomAuthToken(ObtainAuthToken):  # TODO: rename view
    def post(self, request, *args, **kwargs):
        # TODO: update serializer
        updated_data = {
            "username": request.data["email"],
            "password": request.data["password"],
        }
        serializer = self.serializer_class(
            data=updated_data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
            }
        )
