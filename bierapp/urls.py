from django.conf.urls import patterns, include, url
from django.contrib import admin


api_v1_patterns = patterns(
    "",

    url(r"", include("bierapp.api.urls_api_v1")),
)

urlpatterns = patterns(
    "",

    url(r"^", include("bierapp.core.urls")),
    url(r"^", include("bierapp.accounts.urls")),

    url(r"^oauth2/", include("bierapp.oauth2.urls", namespace="oauth2")),
    url(r"^api/v1/", include(api_v1_patterns)),
    url(r"^api/", include(api_v1_patterns)),

    url(r"^admin/doc/", include("django.contrib.admindocs.urls")),
    url(r"^admin/", include(admin.site.urls))
)

# Error handlers
handler403 = "bierapp.views.handler403"
handler404 = "bierapp.views.handler404"
handler500 = "bierapp.views.handler500"
