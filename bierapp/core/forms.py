from django.utils.translation import ugettext_lazy as _
from django import forms

from bierapp.accounts.models import UserMembership, User
from bierapp.core.models import ProductGroup, \
    Product, Transaction, TransactionItem, TransactionTemplate
from bierapp.core.helpers import ProductGroupFormHelper, \
    ProductFormHelper, TransactionFormHelper, \
    InlineTransactionItemFormHelper, DummyFormHelper, InviteGuestFormHelper, \
    ExportFormHelper, PickTemplateFormHelper
from bierapp.utils.fields import GroupedModelChoiceField

import time


class ProductGroupForm(forms.ModelForm):
    helper = ProductGroupFormHelper()

    class Meta:
        model = ProductGroup
        fields = ("title", "is_app_visible")


class ProductForm(forms.ModelForm):
    helper = ProductFormHelper()

    class Meta:
        model = Product
        fields = ("title", "value", "is_app_visible")


class TransactionForm(forms.ModelForm):
    helper = TransactionFormHelper()

    class Meta:
        model = Transaction
        fields = ("description", )

    def __init__(self, site, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)

        self.site = site

    def save(self, commit=True):
        transaction = super(TransactionForm, self).save(commit=False)
        transaction.site = self.site

        if commit:
            transaction.save()

        return transaction


class InlineTransactionItemForm(forms.ModelForm):
    product = GroupedModelChoiceField(Product.objects, "product_group")
    helper = InlineTransactionItemFormHelper

    class Meta:
        model = TransactionItem
        fields = ("product", "count", )

    def __init__(self, product_groups, accounted_user, executing_user=None, *args, **kwargs):
        super(InlineTransactionItemForm, self).__init__(*args, **kwargs)

        self.fields["product"].queryset = Product.objects.filter(product_group__in=product_groups)
        self.accounted_user = accounted_user
        self.executing_user = executing_user if executing_user is not None else accounted_user

    def save(self, commit=True):
        transaction_item = super(InlineTransactionItemForm, self).save(commit=False)

        transaction_item.product_group = self.cleaned_data["product"].product_group
        transaction_item.value = self.cleaned_data["product"].value * self.cleaned_data["count"]
        transaction_item.accounted_user = self.accounted_user
        transaction_item.executing_user = self.executing_user

        if commit:
            transaction_item.save()

        return transaction_item


class ExportForm(forms.Form):

    export_type = forms.ChoiceField(choices=[("csv", "CSV")])
    helper = ExportFormHelper()


class PickTemplateForm(forms.Form):

    template = GroupedModelChoiceField(TransactionTemplate.objects, "category", empty_label=None)
    helper = PickTemplateFormHelper()

    def __init__(self, site, *args, **kwargs):
        super(PickTemplateForm, self).__init__(*args, **kwargs)
        self.fields["template"].queryset = TransactionTemplate.objects.filter(category__site=site)


class DummyForm(forms.Form):
    helper = DummyFormHelper()
