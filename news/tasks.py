from celery import shared_task
from django.utils import timezone
from news.models import News


@shared_task
def publish_scheduled_posts():
    posts = News.objects.filter(
        status='draft',
        scheduled_publication__lte=timezone.now()
    )
    for post in posts:
        post.is_published = True
        post.save()
