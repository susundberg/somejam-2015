# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'nettiapuanyt.urls'

WSGI_APPLICATION = 'nettiapuanyt.wsgi.application'


# Database
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/


TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


SHORT_DATETIME_FORMAT="d.M H:i"

#
# Heroku specific stuff
#
# Parse database configuration from $DATABASE_URL
import dj_database_url

DATABASES = { 'default' : dj_database_url.config() }



# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


#
# This is for local testing
if len(DATABASES["default"]) == 0 :
    DATABASES["default"] = { 
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
          'NAME': 'djangodb',
          'USER': 'www-data',
    }

#
# Local settings
#
INSTALLED_APPS.append("chat_info")
INSTALLED_APPS.append("chat_event")

TEMPLATE_DIRS = ("templates/",)
STATICFILES_DIRS = ("static/",)

TIME_ZONE = "Europe/Helsinki"  
LANGUAGE_CODE = 'fi-fi'
NUSUVEFO_BASE = "http://www.verke.org"

if os.getenv("SECRET_KEY",None) :
     SECRET_KEY = os.environ["SECRET_KEY"] 
     NUSUVEFO_USERNAME = os.environ["NUSUVEFO_USERNAME"] 
     NUSUVEFO_PASSWORD = os.environ["NUSUVEFO_PASSWORD"]
else:
   from settings_secret import *
   
if "SECRET_KEY" not in locals():
  raise Exception("Your settings_secret.py is not valid")




