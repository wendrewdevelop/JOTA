import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "jota.settings"
)

app = Celery("config")

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY"
)
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'publish-scheduled-posts-each-minute': {
        'task': 'news.tasks.publish_scheduled_posts',
        'schedule': crontab(minute='*/1'),  # run each minute
    },
}
