from django.shortcuts import render
from django.db.models import Sum, Count
from django.shortcuts import redirect
from django.forms.models import inlineformset_factory
from django.http import StreamingHttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from datetime import datetime

from bierapp.utils.decorators import json_response
from bierapp.utils.views import paginate

from bierapp.accounts.models import User, UserMembership
from bierapp.core.filters import TransactionFilter, RangeFilter
from bierapp.core.forms import ProductGroupForm, ProductForm, TransactionForm, \
    InlineTransactionItemForm, DummyForm, ExportForm, PickTemplateForm
from bierapp.core.models import Transaction, TransactionItem, ProductGroup, \
    Product
from bierapp.core.decorators import resolve_user, resolve_product, \
    resolve_transaction, resolve_product_group, resolve_template

from cStringIO import StringIO

import csv


@login_required
def index(request):
    if request.site:
        pick_template_form = PickTemplateForm(site=request.site)

        # Last five transactions
        transactions = request \
            .site.transactions \
            .prefetch_related(
                "transaction_items", "transaction_items__accounted_user",
                "transaction_items__executing_user", "transaction_items__product",
                "transaction_items__product_group") \
            .filter(transaction_items__accounted_user=request.user) \
            .order_by("-created") \
            .distinct()[:5]

        # Current balance
        product_groups = list(ProductGroup.objects.filter(site=request.site, transactionitem__accounted_user=request.user).annotate(total_count=Sum("transactionitem__count"), total_value=Sum("transactionitem__value")))

        for product_group in product_groups:
            product_group.all_products = product_group.products.filter(transactionitem__accounted_user=request.user).annotate(total_count=Sum("transactionitem__count"), total_value=Sum("transactionitem__value"))

        return render(request, "bierapp_index.html", locals())
    return render(request, "base_index.html", locals())


@login_required
def help(request):
    return render(request, "bierapp_help.html", locals())


@login_required
def balance_users(request):
    users = request.site.users.all()

    for user in users:
        user.product_groups = list(ProductGroup.objects.filter(site=request.site, transactionitem__accounted_user=user).annotate(total_count=Sum("transactionitem__count"), total_value=Sum("transactionitem__value")))

    return render(request, "bierapp_balance_users.html", locals())


@login_required
@resolve_user
def balance_user(request, user):
    product_groups = list(ProductGroup.objects.filter(site=request.site, transactionitem__accounted_user=user).annotate(total_count=Sum("transactionitem__count"), total_value=Sum("transactionitem__value")))

    for product_group in product_groups:
        product_group.all_products = product_group.products.filter(transactionitem__accounted_user=user).annotate(total_count=Sum("transactionitem__count"), total_value=Sum("transactionitem__value"))

    return render(request, "bierapp_balance_user.html", locals())


@login_required
def balance_products(request):
    user_ids = [str(x.user.pk) for x in UserMembership.objects.filter(site=request.site).order_by("-role")]
    product_group_ids = [str(x.pk) for x in ProductGroup.objects.filter(site=request.site)]

    rows = User.objects.raw(
        """
        SELECT u.*, IFNULL(total_value, 0) AS total_value, IFNULL(total_count, 0) AS total_count, p.id AS product_id, p.product_group_id AS product_group_id
        FROM accounts_user u
        CROSS JOIN core_product p
        LEFT JOIN (
           SELECT accounted_user_id, product_id, SUM(value) AS total_value, SUM(count) AS total_count
           FROM core_transactionitem x, core_transaction y
           WHERE x.transaction_id = y.id AND y.site_id = %d AND x.accounted_user_id IN (%s)
           GROUP BY accounted_user_id, product_id
        ) t ON u.id=t.accounted_user_id AND p.id=t.product_id
        WHERE u.id IN (%s) AND p.product_group_id IN (%s)
        ORDER BY u.id""" % (request.site.pk, ",".join(user_ids), ",".join(user_ids), ",".join(product_group_ids)))

    product_groups = dict((x.pk, x) for x in ProductGroup.objects.filter(pk__in=[ y.product_group_id for y in rows ]))
    products = dict((x.pk, x) for x in Product.objects.filter(pk__in=[ y.product_id for y in rows ]))
    result = {}

    for row in rows:
        product_group = product_groups[row.product_group_id]
        product = products[row.product_id]

        if not product_group in result:
            result[product_group] = {}

        if not product in result[product_group]:
            result[product_group][product] = []

        product.total_count = getattr(product, "total_count", 0) + row.total_count
        product.total_value = getattr(product, "total_value", 0) + row.total_value

        result[product_group][product].append(row)

    users = result.values()[0].values()[0]

    return render(request, "bierapp_balance_products.html", locals())


@login_required
@resolve_product
def balance_product(request, user):
    return render(request, "bierapp_balance_product.html", locals())


@login_required
def transactions(request):
    queryset = request.site.transactions.prefetch_related(
        "transaction_items", "transaction_items__accounted_user",
        "transaction_items__executing_user", "transaction_items__product",
        "transaction_items__product_group").distinct()

    transactions = TransactionFilter(data=request.GET, site=request.site, queryset=queryset)

    form_export = ExportForm()
    form_filter = transactions.form
    transactions = paginate(request, transactions)

    # Export form action should include current GET parameters
    action = reverse("bierapp.core.views.transactions_export") + "?" + request.GET.urlencode()
    form_export.helper.form_action = action

    return render(request, "bierapp_transactions.html", locals())


@login_required
def transactions_export(request):
    queryset = request.site.transactions.prefetch_related(
        "transaction_items", "transaction_items__accounted_user",
        "transaction_items__executing_user", "transaction_items__product",
        "transaction_items__product_group").distinct()

    transactions = TransactionFilter(data=request.GET, site=request.site, queryset=queryset)
    transaction_items = TransactionItem.objects.filter(transaction__in=transactions)

    # Export isn"t a page, so redirect back
    form = ExportForm(data=request.GET or None)

    if not form.is_valid():
        pass # TODO

    # Descide what to do
    export_type = form.cleaned_data["export_type"].lower()

    if export_type == "csv":
        def _inner_to_csv(data):
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(data)

            return output.getvalue()

        def _inner_stream():
            # Export header
            yield _inner_to_csv([
                "Transaction", "Date", "Product", "Product value",
                "Count", "Value", "Accounted user", "Executing user"
            ])

            # Export rows
            for transaction_item in transaction_items.iterator():
                yield _inner_to_csv([
                    transaction_item.transaction_id,
                    transaction_item.transaction.created,
                    transaction_item.product,
                    transaction_item.product.value,
                    transaction_item.count,
                    transaction_item.value,
                    transaction_item.accounted_user,
                    transaction_item.executing_user
                ])

        # Generate streaming response
        response = StreamingHttpResponse(
            streaming_content=_inner_stream(),
            content_type="text/csv; charset=utf-8"
        )

        filename = "transactions_%s.csv" % (datetime.now().strftime("%Y-%m-%d"))
        response["Content-Disposition"] = "attachment; filename=%s" % filename.encode("utf-8")

        # Done
        return response

    return # TODO


@login_required
@resolve_template
def transaction_create(request, template=None):
    class InnerForm(InlineTransactionItemForm):
        def __init__(self, *args, **kwargs):
            product_groups = request.site.product_groups.all()
            super(InnerForm, self).__init__(product_groups=product_groups, accounted_user=request.user, *args, **kwargs)

    TransactionFormSet = inlineformset_factory(Transaction, TransactionItem, form=InnerForm)
    form = TransactionForm(site=request.site, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        transaction = form.save(commit=False)
        formset = TransactionFormSet(data=request.POST, instance=transaction)

        if formset.is_valid():
            transaction.save()
            formset.save()

            # Post message
            messages.success(request, "Transaction added.")

            # Redirect
            return redirect("bierapp.core.views.transactions")

    formset = TransactionFormSet(data=request.POST or None)
    dummy_form = DummyForm()

    # Set template
    if template is not None:
        form.initial = { "description": template.title }
        i = 0

        for pair_item in template.items.all():
            if i < len(formset.forms):
                formset.forms[i].initial = { "product": pair_item.product, "count": pair_item.count }
                i = i + 1
            else:
                break

    # Done
    return render(request, "bierapp_transaction_form.html", locals())


@login_required
@resolve_transaction
def transaction(request, transaction):
    return render(request, "bierapp_transaction.html", locals())


@login_required
def product_groups(request):
    product_groups = request.site.product_groups.annotate(product_count=Count("products"))
    product_groups = paginate(request, product_groups)

    return render(request, "bierapp_product_groups.html", locals())


@login_required
def product_group_create(request):
    form = ProductGroupForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        product_group = form.save(commit=False)
        product_group.site = request.site
        product_group.save()

        # Post message
        messages.success(request, _("Product group added."))

        return redirect(product_group.get_absolute_url())

    return render(request, "bierapp_product_group_create.html", locals())


@login_required
@resolve_product_group
def product_group(request, product_group):
    products = product_group.products.all()
    products = paginate(request, products)

    return render(request, "bierapp_product_group.html", locals())


@login_required
@resolve_product_group
def product_group_product_create(request, product_group):
    form = ProductForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        product = form.save(commit=False)
        product.product_group = product_group
        product.save()

        # Post message
        messages.success(request, _("Product added."))

        return redirect(product.get_absolute_url())

    return render(request, "bierapp_product_group_product_create.html", locals())


@login_required
@resolve_product
def product_group_product(request, product):
    return render(request, "bierapp_product_group_product.html", locals())


@login_required
def stats(request):
    data = request.GET.copy()

    if data.get("after") is None:
        data["after"] = "%d-01-01" % datetime.now().year
    if data.get("before") is None:
        data["before"] = "%d-12-31" % datetime.now().year

    form_range = RangeFilter(data=data, site=request.site).form
    action = reverse("bierapp.core.views.stats_transaction_items") + "?" + data.urlencode()

    return render(request, "bierapp_stats.html", locals())


@login_required
@cache_page(60 * 5)
@json_response
def stats_transaction_items(request):
    transactions = RangeFilter(data=request.GET, site=request.site)

    queryset = TransactionItem.objects \
        .filter(transaction__in=transactions) \
        .prefetch_related("product_group", "executing_user", "product")

    return [{
            "transaction_id": transaction_item.transaction.pk,
            "created": unicode(transaction_item.transaction.created),
            "product_id": transaction_item.product.pk,
            "product": unicode(transaction_item.product),
            "product_group_id": transaction_item.product_group.pk,
            "product_group": unicode(transaction_item.product_group),
            "count": transaction_item.count,
            "value": transaction_item.value,
            "user_id": transaction_item.executing_user.pk,
            "user": unicode(transaction_item.executing_user),
        } for transaction_item in queryset]
