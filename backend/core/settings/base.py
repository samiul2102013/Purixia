from pathlib import Path
from datetime import timedelta
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ── Security ──────────────────────────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY')
AUTH_USER_MODEL = 'users.User'

# ── Apps ──────────────────────────────────────────────────────────────────────
DJANGO_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
]
LOCAL_APPS = [
    'apps.users',
    'apps.catalog',
    'apps.cart',
    'apps.orders',
    'apps.banners',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ── Middleware ─────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

# ── Templates ─────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ── Password validation ────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Internationalisation ───────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Asia/Dhaka'
USE_I18N      = True
USE_TZ        = True

# ── Static & Media ────────────────────────────────────────────────────────────
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL   = '/media/'
MEDIA_ROOT  = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Jazzmin Admin Theme ──────────────────────────────────────────────────────────
JAZZMIN_SETTINGS = {
    'site_title': 'Purixia BD Admin',
    'site_header': 'Purixia BD',
    'site_brand': 'Purixia BD',
    'site_logo': None,
    'login_logo': None,
    'login_logo_dark': None,
    'site_logo_classes': 'img-circle',
    'site_icon': None,
    'welcome_sign': 'Welcome to Purixia BD Admin',
    'copyright': 'Purixia BD',
    'search_model': ['auth.User', 'catalog.Product'],
    'user_avatar': None,
    'topmenu_links': [
        {'name': 'Home', 'url': 'admin:index', 'permissions': ['auth.view_user']},
        {'name': 'View Site', 'url': '/', 'new_window': True},
    ],
    'usermenu_links': [
        {'name': 'View Site', 'url': '/', 'new_window': True, 'icon': 'fas fa-external-link-alt'},
    ],
    'show_sidebar': True,
    'navigation_expanded': True,
    'hide_apps': [],
    'hide_models': [],
    'order_with_respect_to': ['catalog', 'orders', 'banners', 'users', 'auth'],
    'custom_links': {},
    'icons': {
        'auth.User': 'fas fa-users',
        'auth.Group': 'fas fa-users-cog',
        'users.User': 'fas fa-user',
        'catalog.Category': 'fas fa-tags',
        'catalog.Product': 'fas fa-box-open',
        'catalog.ProductImage': 'fas fa-images',
        'orders.Order': 'fas fa-shopping-cart',
        'orders.OrderItem': 'fas fa-receipt',
        'orders.ShippingInfo': 'fas fa-truck',
        'banners.Banner': 'fas fa-ad',
    },
    'default_icon_parents': 'fas fa-chevron-circle-right',
    'default_icon_children': 'fas fa-circle',
    'related_modal_active': True,
    'custom_css': None,
    'custom_js': None,
    'use_google_fonts_cdn': True,
    'show_ui_builder': False,
    'changeform_format': 'horizontal_tabs',
    'changeform_format_overrides': {
        'auth.User': 'collapsible',
        'auth.Group': 'vertical_tabs',
    },
    'language_chooser': False,
}

JAZZMIN_UI_TWEAKS = {
    'navbar_small_text': False,
    'footer_small_text': False,
    'body_small_text': False,
    'brand_small_text': False,
    'brand_colour': 'navbar-warning',
    'accent': 'accent-warning',
    'navbar': 'navbar-white navbar-light',
    'no_navbar_border': True,
    'navbar_fixed': True,
    'layout_boxed': False,
    'footer_fixed': False,
    'sidebar_fixed': True,
    'sidebar': 'sidebar-dark-warning',
    'sidebar_nav_small_text': False,
    'sidebar_disable_expand': False,
    'sidebar_nav_child_indent': True,
    'sidebar_nav_compact_style': False,
    'sidebar_nav_legacy_style': False,
    'sidebar_nav_flat_style': True,
    'theme': 'minty',
    'dark_mode_theme': 'darkly',
    'button_classes': {
        'primary': 'btn-warning',
        'secondary': 'btn-outline-warning',
        'info': 'btn-info',
        'warning': 'btn-warning',
        'danger': 'btn-danger',
        'success': 'btn-success',
    },
    'actions_sticky_top': True,
}

# ── DRF ───────────────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.users.auth.SafeJWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}

# ── JWT ───────────────────────────────────────────────────────────────────────
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':  timedelta(minutes=config('JWT_ACCESS_TOKEN_LIFETIME_MINUTES',  default=60,  cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=config('JWT_REFRESH_TOKEN_LIFETIME_DAYS', default=7,   cast=int)),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
