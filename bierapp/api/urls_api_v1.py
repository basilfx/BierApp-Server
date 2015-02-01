from django.conf.urls import patterns, url

urlpatterns = patterns(
    "",

    url(r"^$", "bierapp.api.views.index"),
    url(r"^transactions/$", "bierapp.api.views.transactions"),
    url(r"^products/$", "bierapp.api.views.products"),
    url(r"^users/info/$", "bierapp.api.views.users_info"),
    url(r"^users/$", "bierapp.api.views.users"),
    url(r"^stats/$", "bierapp.api.views.stats"),
)
