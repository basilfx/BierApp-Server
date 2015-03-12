from django.db.models import Sum

from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions

from bierapp.accounts.models import User
from bierapp.core.filters import TransactionFilter
from bierapp.core.models import Product, Transaction, TransactionItem, \
    XPTransaction
from bierapp.api.serializers import ProductSerializer, TransactionSerializer, \
    UserSerializer, UserInfoSerializer

from itertools import groupby


class ApiIndex(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response({
            "name": request.site.name,
            "users": reverse("bierapp.api.views.users", request=request),
            "products": reverse("bierapp.api.views.products", request=request),
            "transactions": reverse(
                "bierapp.api.views.transactions", request=request),
            "stats": reverse("bierapp.api.views.stats", request=request)
        })


class ProductList(generics.ListAPIView):
    model = Product
    serializer_class = ProductSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        site = self.request.site
        return Product.objects \
                      .filter(product_group__in=site.product_groups.filter(
                          is_hidden=False), is_hidden=False)


class TransactionList(generics.ListCreateAPIView):
    model = Transaction
    serializer_class = TransactionSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return TransactionFilter(
            data=self.request.QUERY_PARAMS, site=self.request.site).qs

    def perform_create(self, serializer):
        serializer.save(site=self.request.site)


class UserList(generics.ListAPIView):
    model = User
    serializer_class = UserSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.site.users \
                           .extra(select={"role": "role"}) \
                           .order_by("role")


class UserInfoList(generics.ListAPIView):
    serializer_class = UserInfoSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def filter_queryset(self, queryset):
        site = self.request.site
        objects = super(UserInfoList, self).filter_queryset(
            site.users.active())

        balances = {}
        mapping = {}
        xps = {}
        result = []

        rows_a = TransactionItem \
            .objects \
            .values(
                "accounted_user", "product", "product__value",
                "product__product_group") \
            .annotate(count=Sum("count")) \
            .annotate(value=Sum("value")) \
            .filter(
                transaction__site=site,
                accounted_user__in=objects.values_list("id")) \
            .order_by("accounted_user")

        rows_b = TransactionItem \
            .objects \
            .values("accounted_user", "product__product_group") \
            .annotate(total_count=Sum("count")) \
            .annotate(total_value=Sum("value")) \
            .filter(
                transaction__site=site,
                accounted_user__in=objects.values_list("id")) \
            .order_by("accounted_user")

        rows_c = XPTransaction \
            .objects \
            .values("user") \
            .annotate(total_value=Sum("value")) \
            .filter(site=site, user__in=objects.values_list("id")) \

        for key, value in groupby(rows_b, key=lambda x: x["accounted_user"]):
            if key not in mapping:
                mapping[key] = {}

            for value2 in value:
                mapping[key][value2["product__product_group"]] = value2

        for key, values in groupby(rows_a, key=lambda x: x["accounted_user"]):
            values = list(values)

            for value in values:
                value.update(mapping[key][value["product__product_group"]])

            balances[key] = values

        for row in rows_c:
            xps[row["user"]] = row["total_value"]

        for user in objects.all():
            result.append({
                "id": user.id,
                "xp": xps.get(user.id, 0),
                "balance": balances.get(user.id, [])
            })

        return result

    def get_queryset(self):
        # We override self.filter_queryset to do the actual work
        pass


class Stats(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        transactions = TransactionFilter(data=request.GET, site=request.site)
        transaction_items = TransactionItem.objects \
            .filter(transaction__in=transactions, count__lt=0) \
            .aggregate(count=Sum("count"))

        return Response({
            "count": transaction_items["count"] or 0
        })


# Expose views
index = ApiIndex.as_view()
transactions = TransactionList.as_view()
products = ProductList.as_view()
users = UserList.as_view()
users_info = UserInfoList.as_view()
stats = Stats.as_view()
