from config.settings.base import *  # NOQA

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-@t6sq6&fwebdtt!njz8-ix*qnq086b6a%#8i#2ct7nz84jw27g"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS += [  # NOQA
    "django_extensions",
    "debug_toolbar",
]

MIDDLEWARE += [  # NOQA
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # NOQA
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR.parent / "static",  # NOQA
]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR.parent / "media"  # NOQA

GRAPH_MODELS = {
    "app_labels": ["shop", "accounts"],
}
