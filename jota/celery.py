# jota/celery.py
import os
from celery.schedules import crontab
from celery import Celery


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'jota.settings'
)

app = Celery('jota')

app.config_from_object(
    'django.conf:settings',
    namespace='CELERY'
)
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'publish-scheduled-posts-each-minute': {
        'task': 'news.tasks.publish_scheduled_posts',
        'schedule': crontab(minute='*/1'),  # a cada 1 minuto
    },
}
