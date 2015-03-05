from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import patterns, url

from bierapp.oauth2.views import Authorize, Redirect, Capture, AccessTokenView

urlpatterns = patterns(
    "",

    url(
        r"^authorize/?$", login_required(Capture.as_view()),
        name="capture"),
    url(
        r"^authorize/confirm/?$", login_required(Authorize.as_view()),
        name="authorize"),
    url(
        r"^redirect/?$", login_required(Redirect.as_view()),
        name="redirect"),
    url(
        r"^access_token/?$", csrf_exempt(AccessTokenView.as_view()),
        name="access_token"),
)
