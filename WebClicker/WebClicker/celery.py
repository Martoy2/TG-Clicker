from __future__ import absolute_import, unicode_literals
import os
import django
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebClicker.settings')
django.setup()

from api.task import update_ticket

app = Celery('WebClicker')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True

app.conf.beat_schedule = {
    'update-ticket-every-minute': {
        'task': 'api.task.update_ticket',
        'schedule': crontab(minute='*/1'),  # каждая минута
    },
}