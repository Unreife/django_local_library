"""
Django settings for locallibrary project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# -----------------------------------------------------
# Paths and environment
# -----------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env if present (e.g. DJANGO_SECRET_KEY, DEBUG, DATABASE_URL, etc.)
load_dotenv(os.path.join(BASE_DIR, ".env"))

# -----------------------------------------------------
# Core settings
# -----------------------------------------------------
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-!tzs*^b&5zz4e)3!3u#+h$6_(y4i!*be!3do18-g@%yi@on)w=",
)

DEBUG = os.environ.get("DEBUG", "False").lower() in ("1", "true", "yes")

# NOTE: use lowercase domain
ALLOWED_HOSTS = [
    "oghuz.pythonanywhere.com",
    "127.0.0.1",
    "localhost",
]

# Trust HTTPS origin for CSRF (scheme+host)
CSRF_TRUSTED_ORIGINS = [
    "https://oghuz.pythonanywhere.com",
]

# -----------------------------------------------------
# Applications
# -----------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "catalog.apps.CatalogConfig",
    "macros.apps.MacrosConfig",
]

# -----------------------------------------------------
# Middleware
# -----------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # static files in production
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "locallibrary.urls"

# -----------------------------------------------------
# Templates
# -----------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "locallibrary.wsgi.application"

# -----------------------------------------------------
# Database
# -----------------------------------------------------
# Default to SQLite; override with DATABASE_URL if provided
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    import dj_database_url

    DATABASES["default"] = dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=500,
        conn_health_checks=True,
    )

# -----------------------------------------------------
# Password validation
# -----------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------------------------------
# Internationalization
# -----------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Istanbul"
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------
# Static files
# -----------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# -----------------------------------------------------
# Security (production)
# -----------------------------------------------------
# Enable these for HTTPS (PythonAnywhere provides HTTPS on your domain)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Strong HSTS (adjust seconds if needed)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

X_FRAME_OPTIONS = "DENY"

# -----------------------------------------------------
# Auth redirects
# -----------------------------------------------------
# Use relative paths so it works both locally and on PA
LOGIN_REDIRECT_URL = "/catalog/"
LOGOUT_REDIRECT_URL = "/catalog/"

# -----------------------------------------------------
# Email (console by default)
# -----------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# -----------------------------------------------------
# Defaults
# -----------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
APPEND_SLASH = True
