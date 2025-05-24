from datetime import datetime
from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
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


@shared_task
def send_notification_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        'noreply@yourdomain.com',
        recipient_list,
        fail_silently=False,
    )
