"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from distutils.command.config import config
from pathlib import Path
import pymysql
import os
import dns.resolver
import yaml
with open('secret.yml', 'r') as f:
    secret = yaml.load(f, Loader=yaml.FullLoader)

pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret['django']['secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'api',
    'djoser',
    'channels',
    'guardian',

    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
AUTH_USER_MODEL = 'api.User'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = secret['smtp']['host']
EMAIL_HOST_USER = secret['smtp']['username']
EMAIL_HOST_PASSWORD = secret['smtp']['password']
EMAIL_PORT = secret['smtp']['port']
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = secret['smtp']['from']

# DOMAIN = '192.168.100.2:8000'
DOMAIN = 'api.bap5.cc'


DJOSER = {
    'LOGIN_FIELD': 'email',
    "USER_CREATE_PASSWORD_RETYPE": True,
    'SEND_ACTIVATION_EMAIL': True,
    'ACTIVATION_URL': 'activation/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/{uid}/{token}',
    'SEND_CONFIRMATION_EMAIL': True,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    "SERIALIZERS": {
        'user': 'api.serializers.userSerializer',
        'current_user': 'api.serializers.userSerializer',
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CSRF_TRUSTED_ORIGINS = ['https://api.bap5.cc']

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # default
    'guardian.backends.ObjectPermissionBackend',
)
WSGI_APPLICATION = 'app.wsgi.application'

ASGI_APPLICATION = 'app.asgi.application'


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [('127.0.0.1', 6379)],
#         },
#     },
# }

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

domain =  secret['account']['domain']
srvInfo = {}
srv_records = dns.resolver.resolve('_sql._tcp.' + domain, 'SRV')
for srv in srv_records:
    srvInfo['port'] = srv.port
port = srvInfo['port']

# domain ="192.168.100.6"
# port = 3002

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'IoTApp_server',
        'USER': secret['account']['username'],
        'PASSWORD': secret['account']['password'],
        'HOST': domain,
        'PORT': port,
        'OPTIONS': {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hant'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
