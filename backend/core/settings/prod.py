from .base import *  # noqa
from decouple import config

DEBUG = False

ALLOWED_HOSTS = ['*']

# ── Database: SQLite (Keeping it built-in as requested) ────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ── CORS ──────────────────────────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# If a specific list is provided in .env, use it instead of wildcard
_cors = config('CORS_ALLOWED_ORIGINS', default='').strip()
if _cors:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [o.strip() for o in _cors.split(',') if o.strip()]

# ── CSRF ──────────────────────────────────────────────────────────────────────
CSRF_TRUSTED_ORIGINS = [
    'https://purixia.vercel.app',
    'https://purixia.kodevio.com',
]

# ── SSL Proxy ─────────────────────────────────────────────────────────────────
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ── Security headers ──────────────────────────────────────────────────────────
SECURE_HSTS_SECONDS            = 31_536_000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD            = True
SECURE_SSL_REDIRECT            = False  # nginx handles SSL termination
SESSION_COOKIE_SECURE          = True
SESSION_COOKIE_SAMESITE        = 'None'
CSRF_COOKIE_SECURE             = True
SECURE_CONTENT_TYPE_NOSNIFF    = True
SECURE_BROWSER_XSS_FILTER      = True
X_FRAME_OPTIONS                = 'DENY'

# ── Static files (WhiteNoise) ─────────────────────────────────────────────────
# WhiteNoise configuration for serving static files in production
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ── Logging ───────────────────────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}