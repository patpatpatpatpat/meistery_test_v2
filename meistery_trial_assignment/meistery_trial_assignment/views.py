import os
import logging
from django.conf import settings
from django.http import HttpResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt


index_file_path = os.path.join(settings.REACT_APP_DIR, "build", "index.html")


def react(request):
    """
    A view to serve the react app by reading the index.html from the
    build  react app and serving it as a Httpresponse.
    """
    try:
        with open(index_file_path) as f:
            return HttpResponse(f.read())
    except FileNotFoundError:
        logging.exception("Production build of app not found")


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # TODO: update serializer
        updated_data = {
            'username':  request.data['email'],
            'password': request.data['password'],
        }
        serializer = self.serializer_class(data=updated_data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
        })