"""
Django settings for Principal project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k8aa%lc!^2ajsc#r*u-wgeue3b*#_h64q18tn9-7^usm+rytpz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.humanize',  # Required for elapsed time formatting
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'principal',
    'yandex_money',
    'bootstrapform',
    'markdown_deux',
    'helpdesk'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
)
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'principal.urls'

# WSGI_APPLICATION = 'principal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/login/'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
LOGGING_DIR = 'logs'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/',
    },

    # this cache backend will be used by django-debug-panel
    'debug-panel': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/debug-panel-cache',
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 200
        }
    }
}
# Yandex Kassa
YANDEX_MONEY_DEBUG = DEBUG
YANDEX_MONEY_SCID = 21375
YANDEX_MONEY_SHOP_ID = 30483
YANDEX_MONEY_SHOP_PASSWORD = 'bYS8jmJhFVi6'
YANDEX_MONEY_FAIL_URL = 'https://127.0.0.1:8000/fail-payment/'
YANDEX_MONEY_SUCCESS_URL = 'https://127.0.0.1:8000/success-payment/'
YANDEX_MONEY_MAIL_ADMINS_ON_PAYMENT_ERROR = True

