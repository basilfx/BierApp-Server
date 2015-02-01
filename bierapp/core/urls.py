from django.conf.urls import patterns, url

urlpatterns = patterns(
    "",

    # Homepage
    url(r"^$", "bierapp.core.views.index"),

    # Balances
    url(r"^balances/users/$", "bierapp.core.views.balance_users"),
    url(r"^balances/products/$", "bierapp.core.views.balance_products"),
    url(r"^balances/users/(?P<id>\d+)/$", "bierapp.core.views.balance_user"),
    url(r"^balances/products/(?P<id>\d+)/$", "bierapp.core.views.balance_product"),

    # Transactions
    url(r"^transactions/$", "bierapp.core.views.transactions"),
    url(r"^transactions/export/$", "bierapp.core.views.transactions_export"),
    url(r"^transactions/create/$", "bierapp.core.views.transaction_create"),
    url(r"^transactions/(?P<id>\d+)/$", "bierapp.core.views.transaction"),

    # Product groups and products
    url(r"^groups/$", "bierapp.core.views.product_groups"),
    url(r"^groups/create/$", "bierapp.core.views.product_group_create"),
    url(r"^groups/(?P<id>\d+)/$", "bierapp.core.views.product_group"),
    url(r"^groups/(?P<id>\d+)/products/create/$", "bierapp.core.views.product_group_product_create"),
    url(r"^groups/(?P<group_id>\d+)/products/(?P<id>\d+)/$", "bierapp.core.views.product_group_product"),

    # Statistics
    url(r"^stats/$", "bierapp.core.views.stats"),
    url(r"^stats/transaction_items.json$", "bierapp.core.views.stats_transaction_items"),

    # Help
    url(r"^help/$", "bierapp.core.views.help"),
)
