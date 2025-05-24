from django.db.models.signals import post_save
from django.dispatch import receiver
from news.models import News
from news.tasks import send_notification_email


@receiver(post_save, sender=News)
def news_post_save(sender, instance, created, **kwargs):
    if created:
        send_notification_email.delay(
            subject=f'Nova Notícia: {instance.title}',
            message=f'Confira: {instance.content[:100]}...',
            recipient_list=['user@example.com']
        )
