# Django settings for spacebook_project project.
import os
from pathlib import Path

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-#5f4fx2)y8tb_&*gko!*7m#e#g(e(=nf)0-7!2u=hp4it=g*)%"
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts.apps.AccountsConfig",
    "social_django",
    "website",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "spacebook_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                "website.context_processors.google_profile_picture",
                "website.context_processors.nav_branches",
            ],
        },
    },
]

WSGI_APPLICATION = "spacebook_project.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    "main": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "main.db",
    },
}

DATABASE_ROUTERS = ["website.db_router.MainRouter"]

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

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kuala_Lumpur"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/spacebook/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/spacebook/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",  # Google
    "django.contrib.auth.backends.ModelBackend",  # normal Django auth
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = (
    "496461563970-jltkj3brmut9ubdcmu7c2fde885ashf0.apps.googleusercontent.com"
)

SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "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"
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ["uitm.edu.my", "student.uitm.edu.my"]


SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = (
    "http://127.0.0.1:8000/spacebook/oauth/complete/google-oauth2/"
)

SOCIAL_AUTH_GOOGLE_OAUTH2_AUTHORIZATION_URL = (
    "https://accounts.google.com/o/oauth2/auth"
)
SOCIAL_AUTH_GOOGLE_OAUTH2_TOKEN_URL = "https://oauth2.googleapis.com/token"

SOCIAL_AUTH_LOGIN_ERROR_URL = "/spacebook/"
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/spacebook/"
SOCIAL_AUTH_USE_NEXT = True


SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]

SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = [
    "sub",
    "email",
    "name",
    "given_name",
    "family_name",
    "picture",
    "locale",
    "hd",
]

LOGIN_URL = "/spacebook/oauth/login/google-oauth2/"
LOGIN_REDIRECT_URL = "/spacebook/"
LOGOUT_REDIRECT_URL = "/spacebook/"
LOGOUT_URL = "/spacebook/accounts/logout/"
