import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
CONF_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.join(CONF_DIR, "../../"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = None

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Core parts
    'bierapp',
    'bierapp.accounts',
    'bierapp.core',
    'bierapp.utils',
    'bierapp.oauth',

    # Third-party
    'django_filters',
    'crispy_forms',
    'crispy_forms_extra',
    'rest_framework',
    'django_extensions',
    'djangobower',
    'custom_user',

    # OAuth 2
    'provider',
    'provider.oauth2'
]

MIDDLEWARE = [
    'bierapp.utils.cache.RequestCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'bierapp.utils.middleware.OAuth2MiddlewareRequest',
    'bierapp.utils.middleware.SiteMiddlewareRequest',
]

ROOT_URLCONF = 'bierapp.urls'

LOGIN_REDIRECT_URL = "/"

AUTH_USER_MODEL = 'accounts.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bierapp.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'database.db'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder'
]

# Media root and URL configuration.

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

MEDIA_URL = "/media/"

# Crispy forms default template pack
CRISPY_TEMPLATE_PACK = "bootstrap3"

# Bower configuration
BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, "bierapp/static/")

BOWER_INSTALLED_APPS = (
    "bootstrap",
    "bootstrap-notify",
    "eonasdan-bootstrap-datetimepicker",
    "dcjs#2.1.5",
    "less.js",
    "jquery"
)

# OAuth2 config
OAUTH_SINGLE_ACCESS_TOKEN = True

# Django REST Framework config
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "bierapp.accounts.authentication.OAuth2PassThruAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    )
}
