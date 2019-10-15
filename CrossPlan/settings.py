"""
Django settings for CrossPlan project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import socket
from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('CP_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('CP_ENV', 'development') == 'development' else False

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "192.168.1.18",
    os.environ.get('CP_ENDPOINT', 'localhost')
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'django_celery_results',
    'channels',
    'fediverse',
    'Web'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CrossPlan.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'Web', 'template')
        ],
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

WSGI_APPLICATION = 'CrossPlan.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('CP_DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('CP_DB_NAME', 'crossplan'),
        'USER': os.environ.get('CP_DB_USER', 'crossplan'),
        'PASSWORD': os.environ.get('CP_DB_PASS', 'password'),
        'HOST': os.environ.get('CP_DB_HOST', 'localhost'),
        'PORT': str(os.environ.get('CP_DB_PORT', '5432')),
        'TEST': {
            'NAME': 'test_crossplan'
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ja-jp'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'fediverse.User'

CELERY_RESULT_BACKEND = 'django-db'

CELERY_BROKER_URL = f'redis://{os.environ.get("CP_REDIS_HOST", "localhost")}:{str(os.environ.get("CP_REDIS_PORT", "6379"))}/1'

CP_ENDPOINT = os.environ.get('CP_ENDPOINT', 'localhost:8000')

ASGI_APPLICATION = 'CrossPlan.routing.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.environ.get('CP_REDIS_HOST', 'localhost'), int(os.environ.get('CP_REDIS_PORT', 6379)))],
        },
    },
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
