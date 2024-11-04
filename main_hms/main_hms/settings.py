from pathlib import Path
import os
import environ
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent

BASE_URL = "http://127.0.0.1:8000"

env = environ.Env()
env_file = os.path.join(BASE_DIR, ".env")
if os.path.exists(os.path.join(BASE_DIR, ".env.local")):
    env_file = os.path.join(BASE_DIR, ".env.local")
environ.Env.read_env(env_file=env_file)

SECRET_KEY = env("SECRET_KEY")

MONGO_INITDB_ROOT_USERNAME = env("MONGO_INITDB_ROOT_USERNAME")
MONGO_INITDB_ROOT_PASSWORD = env("MONGO_INITDB_ROOT_PASSWORD")
MONGO_HOST = env("MONGO_HOST", default="localhost")
MONGO_PORT = int(env("MONGO_PORT", default=27017))
MONGO_DB = env("MONGO_DB", default="chat_db")

DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "users.apps.UsersConfig",
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Другие мои приложения
    "posts.apps.PostsConfig",
    "chat.apps.ChatConfig",
    "api.apps.ApiConfig",
    "payment.apps.PaymentConfig",
    "reg_auth.apps.RegAuthConfig",
    "main_hms",
    # Сторонние приложения
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "channels",
    "django_celery_beat",
    "django_celery_results",
    "django_elasticsearch_dsl",
    "debug_toolbar",
]

ELASTICSEARCH_DSL = {
    "default": {
        "hosts": "http://elasticsearch:9200",
    }
}

ASGI_APPLICATION = "main_hms.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # "debug_toolbar.middleware.show_toolbar",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

INTERNAL_IPS = ["127.0.0.1", "172.17.0.1", "host.docker.internal", "172.19.0.1"]

# import socket

# def get_internal_ips():
#     hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
#     return [ip[:-1] + "1" for ip in ips] + ["127.0.0.1"]

# INTERNAL_IPS = get_internal_ips()

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}

ROOT_URLCONF = "main_hms.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

AUTHENTICATION_BACKENDS = [
    "main_hms.backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": env("ALGORITHM"),
    "SIGNING_KEY": env("SIGNING_KEY"),
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379/1",
    }
}

AUTH_USER_MODEL = "users.User"

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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "logs/main.log",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": False,
        },
        "__main__": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "main_hms": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}


LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"

# SMTP
EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_SSL = env("EMAIL_USE_SSL")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = env("SERVER_EMAIL")
EMAIL_ADMIN = env("EMAIL_ADMIN")

# Celery
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")
CELERY_RESULT_EXTENDED = env("CELERY_RESULT_EXTENDED")
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = env(
    "CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP"
)
CELERY_BEAT_SCHEDULER = env("CELERY_BEAT_SCHEDULER")

# STRIPE
STRIPE_PUBLISHABLE_KEY = env("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")
STRIPE_API_VERSION = env("STRIPE_API_VERSION")
