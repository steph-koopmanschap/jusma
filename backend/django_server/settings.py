"""
Django settings for django_server project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from django.core.management.commands.runserver import Command as runserver
from pathlib import Path
import os
import redis
from dotenv import load_dotenv
load_dotenv()

# Environment varaibles
BACKEND_HOST = os.getenv('BACKEND_HOST')
BACKEND_PORT = os.getenv('BACKEND_PORT')

# This is to allows external services though .env file
MEDIA_ROOT = os.getenv('MEDIA_ROOT')
LOGS_ROOT = os.getenv('LOGS_ROOT')

runserver.default_addr = BACKEND_HOST
runserver.default_port = BACKEND_PORT

if os.getenv('STAGE') == 'production':
    BASE_URL = f'https://{BACKEND_HOST}'
    DEBUG = False
elif os.getenv('STAGE') == 'development':
    BASE_URL = f'http://{BACKEND_HOST}:{BACKEND_PORT}'
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = f"{BASE_URL}/media/"
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Used for signing and hashing cookies and session secrets
SECRET_KEY = os.getenv('SESSION_SECRET')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(LOGS_ROOT, 'server_logfile.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
APPEND_SLASH = False


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'api'
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

REST_FRAMEWORK = {
   "DEFAULT_RENDERER_CLASSES": [
       "api.renderers.JasmaJSONRenderer",
       "rest_framework.renderers.BrowsableAPIRenderer",
    ],
   "EXCEPTION_HANDLER" : "api.exception_handler.jasma_exception_handler",
   'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PROXY_HEADERS': {
        'HTTP_X_FORWARDED_FOR': 'X_FORWARDED_FOR',
    }
}


ROOT_URLCONF = 'django_server.urls'

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

WSGI_APPLICATION = 'django_server.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('PG_HOST'),
        'PORT': os.getenv('PG_PORT')
    }
}

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': os.getenv('DB_NAME'),
#        'USER': os.getenv('PG_SUPER_USER'),
#        'PASSWORD': os.getenv('PG_SUPER_PASSWORD'),
#        'HOST': os.getenv('PG_HOST'),
#        'PORT': os.getenv('PG_PORT'),
#    },
#    'test': {
#    'ENGINE': 'django.db.backends.postgresql',
#    'NAME': "jasma_test_db",
#    'USER': os.getenv('DB_USER'),
#    'PASSWORD': os.getenv('DB_PASSWORD'),
#    'HOST': os.getenv('DB_HOST'),
#    'PORT': os.getenv('DB_PORT'),
#    }
# }

# REDIS Setup
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

REDIS_CLIENT = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_AGE = 86400
SESSION_COOKIE_PATH = '/'
SESSION_COOKIE_SECURE = False  # Send cookie over HTTPS only?
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

AUTH_USER_MODEL = 'api.User'
AUTHENTICATION_BACKENDS = [
    "api.backends.CustomUserModelBackend", "django.contrib.auth.backends.ModelBackend"]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
