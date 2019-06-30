import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COOKIE_DOMAIN = '127.0.0.1'
REDIRECT_URL = 'http://127.0.0.1:9100'
SITE_URL = 'http://127.0.0.1:8000'
MEDIA_URL = 'http://127.0.0.1:8000/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
THUMBNAIL_DEBUG = True
THUMBNAIL_PREFIX = 'cache/'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'uknackdb',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}