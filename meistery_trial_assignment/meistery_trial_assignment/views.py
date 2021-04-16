import os
import logging
from django.conf import settings
from django.http import HttpResponse


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
