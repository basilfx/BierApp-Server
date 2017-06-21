from django.conf.urls import url

from bierapp.core.views import index, balance_users, balance_products, \
    balance_user, balance_product, transactions, transactions_export, \
    transaction_create, transaction, transaction_templates, \
    transaction_template_create, transaction_template, \
    product_groups, product_group_create, product_group, \
    product_group_product_create, product_group_product, stats, \
    stats_transaction_items, help

app_name = 'core'

urlpatterns = [
    # Homepage
    url(r"^$", index, name='index'),

    # Balances
    url(r"^balances/users/$", balance_users, name='balance_users'),
    url(r"^balances/products/$", balance_products, name='balance_products'),
    url(r"^balances/users/(?P<id>\d+)/$", balance_user, name='balance_user'),
    url(
        r"^balances/products/(?P<id>\d+)/$", balance_product,
        name='balance_product'),

    # Transactions and templates
    url(r"^transactions/$", transactions, name='transactions'),
    url(
        r"^transactions/export/$", transactions_export,
        name='transactions_export'),
    url(
        r"^transactions/create/$", transaction_create,
        name='transaction_create'),
    url(r"^transactions/(?P<id>\d+)/$", transaction, name='transaction'),
    url(
        r"^transactions/templates/$", transaction_templates,
        name='transaction_templates'),
    url(
        r"^transactions/templates/create/$", transaction_template_create,
        name='transaction_template_create'),
    url(
        r"^transactions/templates/(?P<id>\d+)/$", transaction_template,
        name='transaction_template'),

    # Product groups and products
    url(r"^groups/$", product_groups, name='product_groups'),
    url(
        r"^groups/create/$", product_group_create,
        name='product_group_create'),
    url(r"^groups/(?P<id>\d+)/$", product_group, name='product_group'),
    url(
        r"^groups/(?P<id>\d+)/products/create/$",
        product_group_product_create, name='product_group_product_create'),
    url(
        r"^groups/(?P<group_id>\d+)/products/(?P<id>\d+)/$",
        product_group_product, name='product_group_product'),

    # Statistics
    url(r"^stats/$", stats, name='stats'),
    url(
        r"^stats/transaction_items.json$", stats_transaction_items,
        name='stats_transaction_items'),

    # Help
    url(r"^help/$", help, name='help'),
]
