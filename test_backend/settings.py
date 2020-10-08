"""
Django settings for test_backend project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import django_heroku
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i0r&c_@!4xd&ze##voyl&l0js-(p^lo)cv+k+7r7s8zfr24zj!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if os.getenv('ENV') == 'PROD' else True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    'core',
    'custom_user',

    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    "log_viewer",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'test_backend.urls'

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

WSGI_APPLICATION = 'test_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME', 'test_backend_db'),
        'USER': os.getenv('DB_USER', 'test_admin'),
        'PASSWORD': os.getenv('DB_PASSWORD', '1996'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


AUTH_USER_MODEL = 'custom_user.CustomUser'


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],

}

########### Integration
COMPANIES_URL = 'http://otp.spider.ru/test/companies/'
PRODUCTS_POSTFIX = '/products/'
TASK_SCHEDULE = 60 * int(os.getenv('INTEGRATION_SCHEDULE_MIN', 1))

########### Celery
CELERY_ALWAYS_EAGER = False
CELERY_BROKER_HOST = os.environ.get('CELERY_BROKER', 'localhost')
CELERY_BROKER_URL = os.getenv('CLOUDAMQP_URL', f'pyamqp://guest@{CELERY_BROKER_HOST}//')
CELERY_BEAT_SCHEDULE = {
    'integration': {
        'task': 'core.tasks.integrate',
        'schedule': TASK_SCHEDULE,
    },
}

######## Static

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

######## Loging

logs_dir = os.path.join(BASE_DIR, 'logs')

if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

LOG_VIEWER_FILES_PATTERN = '*.log'
LOG_VIEWER_FILES_DIR = os.path.join(BASE_DIR, 'logs')
LOG_VIEWER_PATTERNS = ['OFNI']
LOG_VIEWER_MAX_READ_LINES = 1000  # total log lines will be read
LOG_VIEWER_PAGE_LENGTH = 25       # total log lines per-page

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'log_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'backupCount': 1,
            'formatter': 'simple',
            'maxBytes': 16*1000000,
            'filename': 'logs/integration_log.log'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        }
    },
    'loggers': {
        'integration_task': {
            'handlers': ['log_file'],
            'propagate': True,
            'level': 'INFO'
        },
    }
}


django_heroku.settings(locals(), staticfiles=False, test_runner=False, logging=False)
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
