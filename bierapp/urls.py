from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

api_v1_patterns = [
    url(r"", include("bierapp.api.urls_api_v1")),
]

urlpatterns = [
    url(r"^", include("bierapp.core.urls")),
    url(r"^", include("bierapp.accounts.urls")),

    url(r"^oauth2/", include("bierapp.oauth.urls", namespace="oauth2")),
    url(r"^api/v1/", include(api_v1_patterns)),

    url(r"^admin/doc/", include("django.contrib.admindocs.urls")),
    url(r"^admin/", include(admin.site.urls))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.ENABLE_DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

# Error handlers
handler403 = "bierapp.views.handler403"
handler404 = "bierapp.views.handler404"
handler500 = "bierapp.views.handler500"
