# -*- coding: utf-8 -*-
from settings import *
import logging

DEBUG = True

TEMPLATE_DEBUG = DEBUG
DEBUG_PROPAGATE_EXCEPTIONS = DEBUG

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/Users/morytox/Projects/pollsys/sqlite.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# debug-logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# add django devserver if installed
try:
    import devserver
except ImportError:
    pass
else:
    INSTALLED_APPS.append('devserver')


