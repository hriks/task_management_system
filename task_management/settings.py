from __future__ import absolute_import

import os

import redis
from kombu import Queue

BROKER_URL = 'redis://127.0.0.1:6379'
REDIS_POOL = redis.ConnectionPool.from_url(BROKER_URL)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_QUEUES = (
    Queue('celery'),
)

CELERYBEAT_SCHEDULE = {}


CELERY_TIMEZONE = 'Asia/Calcutta'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


STATIC_ROOT = "static"


STATIC_URL = '/static/'


SECRET_KEY = os.environ.get(
    "SECRET_KEY", "AOKQMOASOQAQMMFP_@)$(DKA0-29301c2mix54")

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
    'ws4redis'
]

WEBSOCKET_URL = '/ws/'

WS4REDIS_EXPIRE = 7200

WS4REDIS_PREFIX = 'ws'

WSGI_APPLICATION = 'ws4redis.django_runserver.application'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'task_management.urls'

WS4REDIS_HEARTBEAT = '--heartbeat--'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'core/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ws4redis.context_processors.default'
            ],
        },
    },
]

SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_PREFIX = 'session'


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR + '/media'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DBNAME'),
        'USER': os.environ.get('DBOWNR'),
        'PASSWORD': os.environ.get('DBPSWD'),
        'HOST': os.environ.get('DBHOST'),
        'PORT': '5432',
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True
