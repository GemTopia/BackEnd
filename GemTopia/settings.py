"""
Django settings for BackEnd project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-xnpa)n!c_j#+j$#v4l69%idkmwlg#dk&2=jial+l%8-f0-dvga'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


#RECAPTCHA
RECAPTCHA_PUBLIC_KEY = '6Ld86qcmAAAAALJyRlOtGR4Sf7gpti_TBhRh8wg'
RECAPTCHA_SECRET_KEY = '6Ld86qcmAAAAAD2wamRCeTHNVqQUXyDf68UZzG4y'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_rest_passwordreset',
    'drf_spectacular',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    'captcha',

    # Local apps
    'home.apps.HomeConfig',
    'users.apps.UsersConfig',
    'wallet.apps.WalletConfig',
    'landing.apps.LandingConfig',
    'game.apps.GameConfig',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'GemTopia API',
    'DESCRIPTION': '',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:3000',
# ]
#
# CORS_ALLOWED_HEADERS = [
#     'Authorization',
# ]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'GemTopia.urls'

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

WSGI_APPLICATION = 'GemTopia.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

import db_conf
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': db_conf.NAME,
        'USER': db_conf.USER,
        'PASSWORD': db_conf.PASSWORD,
        'HOST': db_conf.HOST,  
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

# 400 KB
MAX_UPLOAD_IMAGE_SIZE = '419430'

# Email Configs:
import email_conf 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = email_conf.EMAIL_HOST
EMAIL_HOST_USER = email_conf.EMAIL_HOST_USER
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = email_conf.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'GemTopia'


CSRF_TRUSTED_ORIGINS = ['http://api.gem.kveh.ir']