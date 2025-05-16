import uuid
from django.db import models


class News(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    news_id = models.UUIDield(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    subtitle = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    image = FileField(
        upload_to='uploads/%Y/%m/%d/'
    )
    content = models.TextField()
    published_at = models.DateTimeField(
        auto_now_add=True
    )
    author = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='rascunho',  # Valor padrão
        verbose_name='Status'
    )

    class Meta:
        verbose_name = 'news'
        verbose_name_plural = 'news'
        db_table = 'tb_news'