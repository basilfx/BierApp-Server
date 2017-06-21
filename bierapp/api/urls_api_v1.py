from django.conf.urls import url

from bierapp.api.views import index, transactions, products, users_info, \
    users, stats

app_name = "api_v1"

urlpatterns = [
    url(r"^$", index, name="index"),
    url(r"^transactions/$", transactions, name="transactions"),
    url(r"^products/$", products, name="products"),
    url(r"^users/info/$", users_info, name="users_info"),
    url(r"^users/$", users, name="users"),
    url(r"^stats/$", stats, name="stats"),
]
