import os

# Django settings for bierapp project.
INTERNAL_IPS = ("127.0.0.1",)

# Directory paths based on current directory.
CONF_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.join(CONF_DIR, "../../"))

ADMINS = MANAGER = ()

# Test runner for discovering tests
# See https://docs.djangoproject.com/en/dev/topics/testing/advanced/ for more
# information.
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "Europe/Amsterdam"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don"t put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don"t forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "djangobower.finders.BowerFinder"
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

MIDDLEWARE_CLASSES = (
    "bierapp.utils.cache.RequestCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "bierapp.utils.middleware.OAuth2MiddlewareRequest",
    "bierapp.utils.middleware.SiteMiddlewareRequest",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
)

# Bower configuration
BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, "bierapp/static/")

BOWER_INSTALLED_APPS = (
    "bootstrap",
    "bootstrap-notify",
    "eonasdan-bootstrap-datetimepicker",
    "crossfilter#master",
    "dcjs#master",
    "less.js",
    "jquery"
)

# Specifies User as the custom User class for Django to use
AUTH_USER_MODEL = "accounts.User"

# URL to redirect to after login
LOGIN_REDIRECT_URL = "/"

ROOT_URLCONF = "bierapp.urls"

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates".
    # Always use forward slashes, even on Windows.
    # Don"t forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    # Django related
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Core parts
    "bierapp",
    "bierapp.accounts",
    "bierapp.core",
    "bierapp.utils",

    # Third-party
    "django_filters",
    "crispy_forms",
    "crispy_forms_extra",
    "rest_framework",
    "django_extensions",
    "djangobower",
    "custom_user",

    # OAuth 2
    "provider",
    "provider.oauth2",
    "bierapp.oauth2"
)

# Crispy forms default template pack
CRISPY_TEMPLATE_PACK = "bootstrap3"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler"
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    }
}

# OAuth2 config
OAUTH_SINGLE_ACCESS_TOKEN = True

# Django REST Framework config
REST_FRAMEWORK = {
    "PAGINATE_BY": 25,
    "PAGINATE_BY_PARAM": "limit",

    "DEFAULT_AUTHENTICATION_CLASSES": (
        "bierapp.accounts.authentication.OAuth2PassThruAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    )
}

# Only add pickle to this list if your broker is secured from unwanted access.
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
