from django.http import HttpResponseBadRequest, JsonResponse
from django.core.exceptions import PermissionDenied

from functools import wraps


def api_login_required(func):
    @wraps(func)
    def _inner(request, *args, **kwargs):
        if hasattr(request, "user") and request.user.is_authenticated():
            return func(request, *args, **kwargs)
        raise PermissionDenied
    return _inner


def require_ajax(func):
    """
    AJAX request required decorator. Use it in your views:

    @ajax_required
    def my_view(request):
        ....

    """
    @wraps(func)
    def _inner(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return func(request, *args, **kwargs)
    return _inner


def json_response(func):
    @wraps(func)
    def _inner(request, *args, **kwargs):
        return JsonResponse(func(request, *args, **kwargs), safe=False)
    return _inner
