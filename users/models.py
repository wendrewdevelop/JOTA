import uuid
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from httpx._transports import default
from rest_framework.authtoken.models import Token
from jota.managers import CustomUserManager


class User(AbstractUser):
    PLAN_CHOICES = [
        ('info', 'JOTA Info'),
        ('pro', 'JOTA Pro'),
    ]

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
        editable=False
    )
    username = None
    email = models.EmailField(
        'email address', 
        unique=True
    )
    is_staff = models.BooleanField(
        null=True,
        blank=True,
        default=False
    )
    is_writer = models.BooleanField(
        default=False,
        verbose_name='Editor de jornal',
        null=True,
        blank=True
    )
    is_reader = models.BooleanField(
        default=True,
        verbose_name='Leitor do jornal',
        null=True,
        blank=True,
    )
    plan_name = models.CharField(
        max_length=150,
        choices=PLAN_CHOICES,
        default='info',
        verbose_name='Plano de assinatura',
        null=False,
        blank=False
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'tb_user'

@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
