from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    """
    Index handler.
    """
    return render(request, "base_index.html", locals())


def handler403(request):
    """
    Default 403 handler.
    """
    return render(request, "403.html", status=403)


def handler404(request):
    """
    Default 404 handler.
    """
    return render(request, "404.html", status=404)


def handler500(request):
    """
    Default 500 handler.
    """
    return render(request, "500.html", status=500)
