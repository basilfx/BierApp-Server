from django.shortcuts import get_object_or_404
from django.http import Http404

from functools import wraps

from bierapp.accounts.models import User
from bierapp.core.models import Transaction, ProductGroup, Product, \
    TransactionTemplate
from bierapp.utils.types import get_int


def resolve_user(func):
    @wraps(func)
    def _inner(request, id, *args, **kwargs):
        try:
            user = request.site.members.get(id=id)
        except User.DoesNotExist:
            raise Http404

        return func(request, user, *args, **kwargs)
    return _inner


def resolve_transaction(func):
    @wraps(func)
    def _inner(request, id, *args, **kwargs):
        transaction = get_object_or_404(Transaction, pk=id, site=request.site)
        return func(request, transaction, *args, **kwargs)
    return _inner


def resolve_product_group(func):
    @wraps(func)
    def _inner(request, id, *args, **kwargs):
        product_group = get_object_or_404(
            ProductGroup, pk=id, site=request.site)
        return func(request, product_group, *args, **kwargs)
    return _inner


def resolve_product(func):
    @wraps(func)
    def _inner(request, group_id, id, *args, **kwargs):
        product = get_object_or_404(Product, pk=id, product_group=group_id)
        return func(request, product, *args, **kwargs)
    return _inner


def resolve_template(func):
    @wraps(func)
    def _inner(request, *args, **kwargs):
        template_id = get_int(request.GET, "template", default=False)

        if template_id:
            kwargs["template"] = get_object_or_404(
                TransactionTemplate, pk=template_id,
                category__site=request.site)

        return func(request, *args, **kwargs)
    return _inner
