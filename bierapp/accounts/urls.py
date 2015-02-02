from django.conf.urls import patterns

urlpatterns = patterns(
    "",

    # Locations
    (r"^profile/$", "bierapp.accounts.views.profile"),
    (r"^profile/password/$", "bierapp.accounts.views.password"),

    # Registration
    (r"register/$", "bierapp.accounts.views.register"),
    (r"register/done/$", "bierapp.accounts.views.register_done"),

    # Invites
    (r"invites/$", "bierapp.accounts.views.invites"),
    (r"invites/activate/$", "bierapp.accounts.views.invite_activate"),

    # Sites
    (r"sites/$", "bierapp.accounts.views.sites"),
    (r"sites/create/$", "bierapp.accounts.views.site_create"),
    (r"sites/(?P<id>\d+)/$", "bierapp.accounts.views.site"),
    (r"sites/(?P<id>\d+)/switch/$", "bierapp.accounts.views.site_switch"),
    (r"sites/(?P<id>\d+)/invite/$", "bierapp.accounts.views.site_invite"),

    # Authentication
    (r"login/$", "bierapp.accounts.views.login"),
    (r"logout/$", "bierapp.accounts.views.logout"),
)
