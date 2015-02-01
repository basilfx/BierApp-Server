from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from functools import wraps

from bierapp.accounts.models import UserMembership, Site

def resolve_membership(func):
    """
    Decorator which resolves the parameter 'id' to a membership object. It also
    checks for a valid membership. If the parameter could not be resolved, it
    throws a 404 error.
    """

    @wraps(func)
    def _inner(request, id, *args, **kwargs):
        membership = get_object_or_404(UserMembership, site=id, user=request.user)
        return func(request, membership, *args, **kwargs)
    return _inner

def resolve_site(func):
    """
    Decorator which resolves the parameter 'id' to a site object. If the parameter
    could not be resolved, it throws a 404 error.
    """

    @wraps(func)
    def _inner(request, id, *args, **kwargs):
        site = get_object_or_404(Site, id=id)
        return func(request, site, *args, **kwargs)
    return _inner

def site_admin_required(func):
    """
    Raise a PermissionDenied exception if the current user is not a administrator
    for the given membership.
    """

    @wraps(func)
    def _inner(request, membership, *args, **kwargs):
        if membership.is_admin:
            return func(request, membership, *args, **kwargs)
        else:
            raise PermissionDenied
    return _inner