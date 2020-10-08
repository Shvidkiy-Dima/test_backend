import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_backend.settings')

CeleryApp = Celery('test_backend')
CeleryApp.config_from_object('django.conf:settings', namespace='CELERY')
CeleryApp.autodiscover_tasks()
