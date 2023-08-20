from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
# CSRF_COOKIE_SECURE=True
# SESSION_COOKIE_SECURE=True
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1"]
INTERNAL_IPS = ["127.0.0.1"]
ROOT_URLCONF = "seatsight.urls"
WSGI_APPLICATION = "seatsight.wsgi.application"
# ASGI_APPLICATION = "seatsight.asgi.application"
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer"
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
# added manually
STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "utils",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# This key is only used for local development
SECRET_KEY = "ra9&u3&pqg6bzv*3j67%erc99d8zp(hr5u*bo!-kmw55pijn&4"
# KEY_PATH = os.path.join(BASE_DIR, 'utils', '.key')
# with open(KEY_PATH, 'r') as key_file:
#     SECRET_KEY = key_file.read().strip()
# if not SECRET_KEY:
#     raise ValueError("SECRET_KEY not found in the specified file.")


INSTALLED_APPS = [
    # "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # added manually
    "seat_detector",
    # "accounts",
    # "channels"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # added manually
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]