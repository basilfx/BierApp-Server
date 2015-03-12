from rest_framework import serializers

from bierapp.accounts.models import User, Site
from bierapp.core.models import Product, Transaction, TransactionItem

import math


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ("name", )


class ProductSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ["is_hidden"]

    def get_logo(self, product):
        request = self.context["request"]

        if product.logo:
            return request.build_absolute_uri(product.logo.url)


class TransactionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionItem
        exclude = ("id", "transaction", "value")


class TransactionSerializer(serializers.ModelSerializer):
    transaction_items = TransactionItemSerializer(many=True)

    class Meta:
        model = Transaction
        exclude = ("site", )

    def create(self, validated_data):
        transaction_items_data = validated_data.pop("transaction_items")
        transaction = Transaction.objects.create(**validated_data)

        for transaction_item_data in transaction_items_data:
            transaction_item = TransactionItem(
                transaction=transaction, **transaction_item_data)
            transaction_item.save()

        return transaction


class BalanceSerializer(serializers.Serializer):
    product = serializers.ReadOnlyField()
    count = serializers.ReadOnlyField()
    value = serializers.ReadOnlyField()

    estimated_count = serializers.SerializerMethodField()

    def get_estimated_count(self, info):
        try:
            return int(
                math.floor(info["total_value"] / info["product__value"]))
        except ZeroDivisionError:
            return 0


class UserInfoSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()

    xp = serializers.ReadOnlyField()
    balance = BalanceSerializer(many=True)


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id", "first_name", "last_name", "avatar", "avatar_height",
            "avatar_width", "role", "created", "modified")

    def get_avatar(self, user):
        request = self.context["request"]

        if user.avatar:
            return request.build_absolute_uri(user.avatar.url)
