from bierapp.accounts.models import UserMembership, ROLE_ADMIN, ROLE_MEMBER
from bierapp.core.models import Transaction, Product
from bierapp.core.helpers import TransactionFilterHelper, RangeFilterHelper
from bierapp.utils.filters import GroupedModelChoiceFilter

import django_filters as filters


class TransactionFilter(filters.FilterSet):
    """
    """

    product = GroupedModelChoiceFilter(
        queryset=Product.objects, group_by_field="product_group",
        name="transaction_items__product")

    accounted_user = GroupedModelChoiceFilter(
        group_by_field="role",
        group_label={1: "Admins", 2: "Members", 3: "Guests"},name="transaction_items__accounted_user")
    executing_user = GroupedModelChoiceFilter(
        group_by_field="role",
        group_label={1: "Admins", 2: "Members", 3: "Guests"},name="transaction_items__executing_user")

    before = filters.DateFilter(name="created", lookup_type="lte")
    after = filters.DateFilter(name="created", lookup_type="gte")

    description = filters.CharFilter(
        name="description", lookup_type="icontains")

    class Meta:
        model = Transaction
        fields = ("after", "before", "description", "product",
                  "accounted_user", "executing_user")

    def __init__(self, site, *args, **kwargs):
        super(TransactionFilter, self).__init__(*args, **kwargs)

        users = site.users \
                    .extra(select={"role": "role"}) \
                    .order_by("role")

        self.filters["accounted_user"].extra["queryset"] = users
        self.filters["executing_user"].extra["queryset"] = users

        self.filters["product"].extra["queryset"] = \
            Product.objects \
                   .filter(product_group__in=site.product_groups.all()) \
                   .prefetch_related("product_group")

    @property
    def form(self):
        if not hasattr(self, "_form"):
            super(TransactionFilter, self).form.helper = \
                TransactionFilterHelper()
        return self._form


class RangeFilter(filters.FilterSet):
    """
    """

    before = filters.DateTimeFilter(name="created", lookup_type="lte")
    after = filters.DateTimeFilter(name="created", lookup_type="gte")

    description = filters.CharFilter(
        name="description", lookup_type="icontains")

    class Meta:
        model = Transaction
        fields = ("after", "before", "description")

    def __init__(self, site, *args, **kwargs):
        super(RangeFilter, self).__init__(*args, **kwargs)

    @property
    def form(self):
        if not hasattr(self, "_form"):
            super(RangeFilter, self).form.helper = RangeFilterHelper()
        return self._form
