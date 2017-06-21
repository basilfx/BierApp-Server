from django.conf.urls import url

from bierapp.accounts.views import profile, password, register, \
    register_done, invites, invite_activate, sites, site_create, site, \
    site_switch, site_invite, site_invite_revoke, site_membership_edit, \
    login, logout


app_name = 'accounts'

urlpatterns = [
    # Locations
    url(r"^profile/$", profile, name='profile'),
    url(r"^profile/password/$", password, name='password'),

    # Registration
    url(r"register/$", register, name='register'),
    url(r"register/done/$", register_done, name='register_done'),

    # Invites
    url(r"invites/$", invites, name='invites'),
    url(r"invites/activate/$", invite_activate, name='invite_activate'),

    # Sites
    url(r"sites/$", sites, name='sites'),
    url(r"sites/create/$", site_create, name='site_create'),
    url(r"sites/(?P<site_id>\d+)/$", site, name='site'),
    url(r"sites/(?P<site_id>\d+)/switch/$", site_switch, name='site_switch'),
    url(r"sites/(?P<site_id>\d+)/invite/$", site_invite, name='site_invite'),
    url(r"sites/(?P<site_id>\d+)/invite/(?P<invite_id>\d+)/revoke/$",
        site_invite_revoke, name='site_invite_revoke'),
    url(r"sites/(?P<site_id>\d+)/membership/(?P<membership_id>\d+)/edit/$",
        site_membership_edit, name='site_membership_edit'),

    # Authentication
    url(r"login/$", login, name='login'),
    url(r"logout/$", logout, name='logout'),
]
