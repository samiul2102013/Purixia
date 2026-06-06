from .base import *  # noqa

DEBUG = False

ALLOWED_HOSTS = ['*']

# ── Fast in-memory DB ─────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':   ':memory:',
    }
}

# ── Skip real migrations for speed ────────────────────────────────────────────
# Uncomment if you install pytest-django + django-test-without-migrations
# MIGRATION_MODULES = {app: None for app in LOCAL_APPS}  # noqa: F405

# ── Faster password hashing in tests ──────────────────────────────────────────
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']


# ── Media: temp folder ────────────────────────────────────────────────────────
import tempfile
MEDIA_ROOT = tempfile.mkdtemp()

CORS_ALLOW_ALL_ORIGINS = True