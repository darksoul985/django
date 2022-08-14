from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta


class ShopUser(AbstractUser):
    avatar = models.ImageField(
        verbose_name='Аватарка',
        upload_to='user',
        blank=True
    )
    age = models.PositiveIntegerField(verbose_name='Возраст')
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный пльзователь'
    )
    activation_key = models.CharField(
        max_length=128,
        blank=True
    )
    activation_key_expires = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )

    def is_activation_key_expired(self):
        """ checking the activation pass by mail """
        now_date = now() - timedelta(hours=48)
        if now_date <= self.activation_key_expires:
            return False
        return True
