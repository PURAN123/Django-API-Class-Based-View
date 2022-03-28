
from pathlib import Path
import os
from .info import *
import sys
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6556%m@j272$#td_3-30!9@63b#txxh-w2qu(^03x!bhf-sjt!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Email Addresses and data

EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST=EMAIL_HOST
EMAIL_HOST_USER=EMAIL_HOST_USER
EMAIL_HOST_PASSWORD=EMAIL_HOST_PASSWORD
EMAIL_PORT=EMAIL_PORT


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    "rest_framework",
    
    # project app name
    "ums",

    # Third party apps
    "rest_framework.authtoken",
    "rest_auth",
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'allauth.socialaccount',
    "django_filters",
]

SITE_ID = 1

AUTH_USER_MODEL="ums.User"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'userms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],
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

WSGI_APPLICATION = 'userms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

if "test" in sys.argv:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME':"usermanagementsystem",
            "USER":"root",
            "PASSWORD":"puran",
            "HOST":"localhost",
            "PORT":3306,
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

"""
Add default permission classes and permission classes to the app
"""

REST_FRAMEWORK = {
    "NON_FIELD_ERRORS_KEY": "errors",
    'DEFAULT_AUTHENTICATION_CLASSES': [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
}