"""
Django settings for django_web_app project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import structlog
from corsheaders.defaults import default_headers, default_methods
import logging

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@5&-q%^o=@mb@=@e%b9yz^b#l-2)w&_s0ick#=wy3kw36$z($g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]
#wstawić adres zewnętrzny!!!!!!!!!!!!!!!!!

# Allow cookies only for server inside
SESSION_COOKIE_HTTPONLY = True

# Application definition

PROJECT_APPS = (
    'django_web_app',
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
)

THIRD_PARTY_APPS = (
    'axes',
    'captcha',
    'corsheaders',
    'crispy_forms',
    'password_strength',
)

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

INSTALLED_APPS = PROJECT_APPS + DJANGO_APPS + THIRD_PARTY_APPS

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

MIDDLEWARE = [
    'django_structlog.middlewares.RequestMiddleware',
    'django_web_app.middlewares.RequestResponseLogMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware'
]

MIDDLEWARE_CLASSES = (
    MIDDLEWARE
)

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_HEADERS = default_headers
CORS_ALLOW_METHODS = default_methods

ROOT_URLCONF = 'django_web_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

WSGI_APPLICATION = 'django_web_app.wsgi.application'


LOGLEVEL = "INFO"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        "json_renderer": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(sort_keys=True),
        },
        "console_renderer": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(colors=False),
        },
        "key_value_renderer": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.KeyValueRenderer(key_order=['timestamp', 'level', 'event', 'logger']),
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json_renderer",
        },
        'gunicorn': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'json_renderer',
        }
    },
    'loggers': {
        'base': {
            'level': LOGLEVEL,
            'propagate': False,
            'handlers': ['console'],
        },
    }
}

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = (
    {'NAME': 'django_web_app.password_validation.CustomPasswordValidator'},
)

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT= os.path.join(BASE_DIR, 'static'),

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'blog-home'
LOGIN_URL = 'login'

AXES_COOLOFF_TIME = 1  # h
AXES_WHITELIST_CALLABLE = lambda request, credentials: not credentials.get('username')
AXES_LOCK_OUT_BY_USER_OR_IP = True
AXES_FAILURE_LIMIT = 10
AXES_ENABLED = 1
AXES_ONLY_USER_FAILURES = 1

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']
