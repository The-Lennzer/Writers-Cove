from __future__ import absolute_import, unicode_literals
import os
from writerscove.celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'writerscove.settings')

app = Celery('writerscove')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
