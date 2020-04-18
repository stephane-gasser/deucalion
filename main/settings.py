# Django settings

DEBUG = False
TEMPLATE_DEBUG = DEBUG
SERVE_MEDIA = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

import logging, os, sys
gettext = lambda s: s

## container directory
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), os.path.pardir) 

DATABASES = {
    'default': {
        'ENGINE': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-fr'

LANGUAGES = [
  ("fr", "French"),
]

USE_L10N = True

FORMAT_MODULE_PATH = 'formats'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, "main", 'static'), ## global css, etc.
    )

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'gwbet&h4%a1h7srifskwjo+kezufg1^#4%14hp4p$+y-dm#g5h'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "main", "templates"),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'main.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
     "django.contrib.auth.context_processors.auth",
     "django.core.context_processors.debug",
     "django.core.context_processors.i18n",
     "django.core.context_processors.media",
     "django.core.context_processors.static",
     "django.core.context_processors.tz",
     'django.core.context_processors.request',
     "django.contrib.messages.context_processors.messages",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',

    'filebrowser',
    'wymeditor_fix',
    'wymeditor',
    'grappelli',
    'django.contrib.admin',

    'django_extensions',
    'south',
    'pipeline',
    'bootstrap_toolkit',
#    'polymorphic',
    'sorl.thumbnail',


    'main.Profiles',
#    'main.Solutions',
    'main.Content',
    'main.Messages',
)

PIPELINE = True
PIPELINE_VERSION = True
PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None
PIPELINE_DISABLE_WRAPPER = True
PIPELINE_CSS = {
  'all': {
    'source_filenames': (
      'css/bootstrap-responsive.css',
      'css/styles.css',
      ),
    'output_filename': 'css/compressed.?.css',
    'extra_context': {
      'media': 'screen,projection',
      },
    },
  }

PIPELINE_JS = {
  'all': {
    'source_filenames': (
      'js/jquery-1.9.1.min.js',
      'js/bootstrap.min.js',
      ),
    'output_filename': 'js/compressed.?.js',
    },
}

LOGIN_REDIRECT_URL = "/"

AUTH_PROFILE_MODULE = 'Profiles.Profile'

GRAPPELLI_ADMIN_TITLE = "Deucalion"

DEFAULT_FROM_EMAIL = "messages@deucalion.net"
EMAIL_SUBJECT_PREFIX = ""

DISCLOSURE_COST = 2

## ## https://gist.github.com/889965
## from imp import find_module
## STATICFILES_DIRS = (
##     ('', os.path.join(os.path.abspath(find_module("tinymce")[1]), 'media')),
## )

BOOTSTRAP_CSS_URL = STATIC_URL + "css/bootstrap.min.css"

## local settings
try:
    from local_settings import *
except ImportError:
    pass
except Exception, e:
    logging.warning("local_settings.py not loaded: %s"%e)
    raise e

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'console': {
            'format': '%(asctime)s [%(levelname)7s] (%(name)s) %(message)s'
        },
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },        
    },
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'console'
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_ROOT, "django.log"),
            'maxBytes': 100*(1024**2),
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django.db.backends':{
            'handlers':['logfile'],
            'propagate':False
            },
        '':{
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            },
        }
    }

