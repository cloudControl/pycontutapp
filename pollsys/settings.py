# Django settings for pollsys project.
import dj_database_url
import os
import json
from datetime import timedelta
import newrelic.agent

try:
    json_data = open(os.environ["CRED_FILE"])
    data = json.load(json_data)
    postgrecreds = data['ELEPHANTSQL']
    amqpcreds = data['CLOUDAMQP']
    sendgridcreds = data['SENDGRID']
    memcachecreds = data['MEMCACHIER']
    DATABASES = {'default': dj_database_url.config(default=postgrecreds['ELEPHANTSQL_URL'])}

    os.environ['MEMCACHE_USERNAME'] = memcachecreds['MEMCACHIER_USERNAME']
    os.environ['MEMCACHE_PASSWORD'] = memcachecreds['MEMCACHIER_PASSWORD']

    CACHES = {
        'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': memcachecreds['MEMCACHIER_SERVERS'],
        'TIMEOUT': 500,
        'BINARY': True,
        }
    }

    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = sendgridcreds['SENDGRID_USERNAME']
    EMAIL_HOST_PASSWORD = sendgridcreds['SENDGRID_PASSWORD']
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    json_data.close()
except IOError:
    print 'Clould not open file'
except Exception:
    print 'prepare Local Config'
    DATABASES = {
            'default': {
            'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': '/Users/morytox/Projects/pollsys/sqlite.db',                      # Or path to database file if using sqlite3.
            'USER': '',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            }
    }

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

newrelic_environment = 'production'
newrelic.agent.initialize(os.path.join(SITE_ROOT, '..', 'newrelic.ini'), newrelic_environment)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Felix Knoepke', 'fk+pycon@cloudcontrol.de'),
)

MANAGERS = ADMINS

#DATABASES = {
#            'default': {
#            'ENGINE': 'django.db.backends.mysql',  #'django.db.backends.sqlite3', Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#            'NAME': sqlscreds['MYSQLS_DATABASE'],                      # Or path to database file if using sqlite3.
#            'USER': sqlscreds['MYSQLS_USERNAME'],                      # Not used with sqlite3.
#            'PASSWORD': sqlscreds['MYSQLS_PASSWORD'],                  # Not used with sqlite3.
#            'HOST': sqlscreds['MYSQLS_HOSTNAME'],                      # Set to empty string for localhost. Not used with sqlite3.
#            'PORT': sqlscreds['MYSQLS_PORT'],                      # Set to empty string for default. Not used with sqlite3.
#            }
#}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'de-de'

SITE_ID = 1

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'rpqdmyhjah%@ip@9ee#0x*m=pcfip%rja=)(@nz8how2wqkv)u'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pollsys.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'pollsys.wsgi.application'

TEMPLATE_DIRS = (
    './templates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'polls',
    'gunicorn',
    'client',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
