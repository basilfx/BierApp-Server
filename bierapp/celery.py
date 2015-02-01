from __future__ import absolute_import

from django.conf import settings

from celery import Celery

import os


# Set the default Django settings module for the "celery" program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bierapp.settings.local")

# Using a string here means the worker will not have to pickle the object
# when using Windows.
app = Celery("bierapp")

app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
