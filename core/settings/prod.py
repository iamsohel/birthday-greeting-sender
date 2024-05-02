import os
import dj_database_url
from .common import *

DEBUG = False

CORS_ALLOWED_ORIGINS = [
    "https://prod_url"
]

CSRF_TRUSTED_ORIGINS = [
    "https://prod_url"
]

SECRET_KEY = os.environ['SECRET_KEY']

DATABASES = {
    'default': dj_database_url.config()
}

REDIS_URL = os.environ['REDIS_URL']

CELERY_BROKER_URL = REDIS_URL

DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']

EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASSWORD']
EMAIL_PORT = os.environ['EMAIL_PORT']
