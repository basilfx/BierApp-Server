from bierapp.accounts.models import User
from bierapp.core.models import Transaction, Product
from bierapp.core.helpers import TransactionFilterHelper, RangeFilterHelper
from bierapp.utils.filters import GroupedModelChoiceFilter

import django_filters as filters


class TransactionFilter(filters.FilterSet):
    product = GroupedModelChoiceFilter(queryset=Product.objects, group_by_field="product_group", name="transaction_items__product")

    accounted_user = filters.ModelChoiceFilter(queryset=User.objects, name="transaction_items__accounted_user")
    executing_user = GroupedModelChoiceFilter(queryset=User.objects.order_by("user_type"), group_by_field="user_type", group_label={0: "Inhabitants", 1: "Guests"}, name="transaction_items__executing_user")

    before = filters.DateFilter(name="date_created", lookup_type="lte")
    after = filters.DateFilter(name="date_created", lookup_type="gte")

    description = filters.CharFilter(name="description", lookup_type="icontains")

    class Meta:
        model = Transaction
        fields = ("after", "before", "description", "product", "accounted_user", "executing_user")

    def __init__(self, site, *args, **kwargs):
        super(TransactionFilter, self).__init__(*args, **kwargs)

        self.filters["accounted_user"].extra["queryset"] = site.users
        self.filters["executing_user"].extra["queryset"] = site.users
        self.filters["product"].extra["queryset"] = Product.objects.filter(product_group__in=site.product_groups.all())

    @property
    def form(self):
        if not hasattr(self, "_form"):
            super(TransactionFilter, self).form.helper = TransactionFilterHelper()
        return self._form


class RangeFilter(filters.FilterSet):
    before = filters.DateTimeFilter(name="date_created", lookup_type="lte")
    after = filters.DateTimeFilter(name="date_created", lookup_type="gte")

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
