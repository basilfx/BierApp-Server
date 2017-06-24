import os
import sys


# Append path with this project and libraries.
sys.path.insert(
    0, os.path.join(os.path.abspath(os.path.dirname(__file__)), "../"))
sys.path.insert(
    1, os.path.join(os.path.abspath(os.path.dirname(__file__)), "../lib/"))

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "x.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bierapp.settings.local")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
