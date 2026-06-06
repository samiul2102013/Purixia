from .base import *  # noqa
from decouple import config

DEBUG = True

ALLOWED_HOSTS = ['*']

# ── Database: SQLite for fast local dev ───────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ── CORS: allow Next.js frontend locally ──────────────────────────────────────
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:3001',
    'http://127.0.0.1:3001',
]
CORS_ALLOW_CREDENTIALS = True

# ── Session cookie settings for cross-origin dev ──────────────────────────────
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_HTTPONLY = True

# ── DRF: add Browsable API in dev only ────────────────────────────────────────
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (  # noqa: F405
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)

# ── Django Debug Toolbar (optional — install separately) ──────────────────────
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
# INTERNAL_IPS = ['127.0.0.1']