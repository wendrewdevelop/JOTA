from datetime import datetime
from celery import shared_task
from django.utils import timezone
from .models import News


@shared_task
def publish_scheduled_posts():
    posts = News.objects.filter(
        status='draft',
        scheduled_post__lte=timezone.now()
    )
    for post in posts:
        post.status = 'published'
        post.published_at = timezone.now()
        post.save()
