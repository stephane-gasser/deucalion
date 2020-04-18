DEBUG = True
TEMPLATE_DEBUG = DEBUG
SERVE_MEDIA = True
CACHE_BACKEND = 'dummy://'
PIPELINE = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'deucalion_prod',      # Or path to database file if using sqlite3.
        'USER': 'deucalion_prod',                      # Not used with sqlite3.
        'PASSWORD': 'jibIbcep0',                  # Not used with sqlite3.
        'HOST': 'mysql1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


EMAIL_HOST = "smtp.alwaysdata.com"
EMAIL_HOST_USERNAME = "messages@deucalion.net"
EMAIL_HOST_PASSWORD = "pebAphed6"
