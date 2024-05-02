import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')

celery = Celery('birthday_greeting_sender')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()
