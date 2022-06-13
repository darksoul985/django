from django.db import models
from django.contrib.auth.models import AbstractUser


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
